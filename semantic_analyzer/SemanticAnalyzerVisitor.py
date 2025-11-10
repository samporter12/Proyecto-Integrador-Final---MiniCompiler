from generated.gramaticaVisitor import gramaticaVisitor
from generated.gramaticaParser import gramaticaParser
from semantic_analyzer.IntermediateRepresentation import IR

class SymbolTable:
    def __init__(self):
        self.tasks = {}
        self.variables = {}
        # Mapeamos nombres de tareas a etiquetas TAC (ej: 'inicio' -> 'L_inicio')
        self.task_labels = {} 

    def define_task(self, name, node, label):
        # Primero, la validación semántica crítica: no permite tareas duplicadas
        if name in self.tasks:
            raise Exception(f"Error Semántico: Tarea '{name}' ya está definida.")
        self.tasks[name] = node
        self.task_labels[name] = label # Guardamos la etiqueta

    def define_variable(self, name, node):
        # aquí simplificamos la tabla.
        self.variables[name] = node

    def check_task_exists(self, name):
        # Esta es la validación que usamos en 'visitTransition'.
        if name not in self.tasks:
            raise Exception(f"Error Semántico: Intento de 'ir_a' a tarea no definida: '{name}'.")

    def check_variable_exists(self, name):
        # Esta validación es crucial para las condiciones: si una variable no fue asignada,
        if name not in self.variables:
            raise Exception(f"Error Semántico: Variable no definida '{name}' usada en condición.")

    def get_task_label(self, name):
        """Devuelve la etiqueta TAC para una tarea."""
        # Se asegura de que la tarea exista antes de devolver su etiqueta.
        self.check_task_exists(name) 
        return self.task_labels[name]


class SemanticAnalyzerVisitor(gramaticaVisitor):
    # Este Visitor implementa tanto la Fase 3 (Validación) como la Fase 4 (Generación de Código Intermedio).
    def __init__(self):
        self.symbol_table = SymbolTable()
        # El visitor ahora tiene su propio generador de IR
        self.ir = IR()
        self.current_task_transitions = [] # Almacén temporal para las transiciones

    def visitProgram(self, ctx:gramaticaParser.ProgramContext):
        # PRIMERA PASADA: Recolección de definiciones (igual que antes) 
        
        # 1. Bucle de Tareas:
        # Recorre todos los nodos hijos del programa.
        for item in ctx.getChildren():
            # Si el nodo es una 'tarea'
            if isinstance(item, gramaticaParser.TaskContext):
                # ...saca su nombre y su etiqueta, y los GUARDA en la SymbolTable.
                task_name = item.ID().getText()
                # Creamos etiquetas TAC descriptivas (ej: L_TAREA_inicio).
                task_label = f"L_TAREA_{task_name}" 
                self.symbol_table.define_task(task_name, item, task_label)

        # 2. Recolección de variables (Definición)
        for item in ctx.getChildren():
            # Si es una tarea, mira DENTRO de ella
            if isinstance(item, gramaticaParser.TaskContext):
                for stmt in item.statement():
                    if stmt.assignment_stmt():
                        var_name = stmt.assignment_stmt().ID().getText()
                        self.symbol_table.define_variable(var_name, stmt)
        
        # 3. Recolección de transiciones (Las asignamos a la tarea anterior)
        # Esto nos permite saber qué 'ir_a' debe ejecutarse al final de qué 'tarea'.
        last_task_name = None
        temp_transitions = {}
        for item in ctx.getChildren():
            # Lógica para mapear transiciones a la tarea previa
            if isinstance(item, gramaticaParser.TaskContext):
                last_task_name = item.ID().getText()
                if last_task_name not in temp_transitions:
                    temp_transitions[last_task_name] = []
            elif isinstance(item, gramaticaParser.TransitionContext):
                if last_task_name:
                    temp_transitions[last_task_name].append(item)
                else:
                    raise Exception("Error Semántico: 'ir_a' sin 'tarea' previa.")
        
        self.task_transitions_map = temp_transitions

        # SEGUNDA PASADA: Validación y Generación de IR 
        # En lugar de llamar a self.visitChildren(ctx) (que visita TAREAS y TRANSICIONES),
        # iteramos manualmente y visitamos SOLO las TAREAS.
        # Nuestras tareas (visitTask) ahora son responsables de
        # visitar sus propias transiciones.
        
        for item in ctx.getChildren():
            if isinstance(item, gramaticaParser.TaskContext):
                self.visit(item) # Llama a visitTask
        
        return 

    def visitTask(self, ctx:gramaticaParser.TaskContext):
        task_name = ctx.ID().getText()
        task_label = self.symbol_table.get_task_label(task_name)
        
        #  Generar TAC 
        self.ir.add_instruction(op=f"{task_label}:") # Etiqueta de inicio de tarea
        
        # 2. Generación del TAC para el cuerpo (Statements: print, assign)
        self.visitChildren(ctx) 
        
        # 3. Generación del TAC para las transiciones (los 'ir_a' que van después de esta tarea)
        if task_name in self.task_transitions_map:
            for transition_node in self.task_transitions_map[task_name]:
                self.visit(transition_node) # Esto llama a visitTransition.
        
        # 4. Fin de la Tarea en el TAC
        self.ir.add_instruction(op='RETURN') # Todas las tareas deben terminar con un RETURN.
        self.ir.add_instruction(op='') # Línea en blanco para legibilidad en la salida.
        return

    def visitTransition(self, ctx:gramaticaParser.TransitionContext):
        target_task_name = ctx.ID().getText()
        # Ya validamos que exista, ahora obtenemos su etiqueta TAC de la tabla de símbolos.
        target_label = self.symbol_table.get_task_label(target_task_name)
        
        # Generar TAC 
        # 1. Visitar la condición, que devolverá el 'temp' (ej: t1)
        temp_var = self.visit(ctx.condition()) 
        
        # 2. Creamos la etiqueta a donde saltaremos si la condición es falsa.
        skip_label = self.ir.new_label()
        
        # 3. La instrucción clave: si la temporal es falsa, ignoramos la llamada y saltamos a L1.
        self.ir.add_instruction(op='if_false_goto', arg1=temp_var, result=skip_label)
        
        # 4. Si es VERDADERA, ejecutamos la llamada a la tarea destino.
        self.ir.add_instruction(op='CALL', result=target_label) 
        
        # 5. Marcamos el punto de salto (L1:), donde continúa el flujo si la condición fue falsa.
        self.ir.add_instruction(op=f"{skip_label}:")
        return 

    def visitAssignment_stmt(self, ctx:gramaticaParser.Assignment_stmtContext):
        var_name = ctx.ID().getText()
        value = ctx.VALUE().getText()
        
        # Generar TAC 
        # estado = "OK"
        self.ir.add_instruction(op='=', arg1=value, result=var_name)
        return

    def visitPrint_stmt(self, ctx:gramaticaParser.Print_stmtContext):
        value = ctx.VALUE().getText()
        
        # Generar TAC 
        # PRINT "Comenzando"
        self.ir.add_instruction(op='PRINT', arg1=value)
        return

    def visitCondition(self, ctx:gramaticaParser.ConditionContext):
        # 1. Verificación semántica: ¿La variable fue definida?
        var_name = ctx.ID().getText()
        self.symbol_table.check_variable_exists(var_name)
        
        op = ctx.comparator().getText()
        value = ctx.VALUE().getText()

        # Generar TAC 
        # 1. Generar una variable temporal para el resultado
        temp_var = self.ir.new_temp()
        
        # El TAC compara los valores y guarda el booleano en t1 (ej: t1 = estado == "OK").
        self.ir.add_instruction(op=op, arg1=var_name, arg2=value, result=temp_var)
        
        # Devolvemos la variable temporal para que visitTransition pueda usarla en el 'if_false_goto'.
        return temp_var