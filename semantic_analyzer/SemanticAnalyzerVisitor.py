from generated.gramaticaVisitor import gramaticaVisitor
from generated.gramaticaParser import gramaticaParser
from semantic_analyzer.IntermediateRepresentation import IR

class SymbolTable:
    # Esta es la tabla de símbolos. Es el corazón de la Fase 3.
    # Mantiene el registro de todos los identificadores (tareas y variables) del programa.
    def __init__(self):
        self.tasks = {}        # Diccionario para almacenar las tareas definidas (y prevenir duplicados).
        self.variables = {}    # Diccionario para rastrear las variables que reciben una asignación.
        self.task_labels = {}  # Mapea el nombre de la tarea 'inicio' a su etiqueta TAC 'L_TAREA_inicio'.

    def define_task(self, name, node, label):
        # Primero, la validación semántica crítica: no permite tareas duplicadas
        if name in self.tasks:
            raise Exception(f"Error Semántico: Tarea '{name}' ya está definida.")
        self.tasks[name] = node
        # Y registramos su etiqueta TAC, que será usada en las llamadas 'ir_a'.
        self.task_labels[name] = label 

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
        self.ir = IR() # Instancia de la Representación Intermedia para almacenar el TAC.
        self.current_task_transitions = [] 
        # Este mapa guarda las transiciones asociadas a cada tarea antes de generar el TAC.
        self.task_transitions_map = {} 

    def visitProgram(self, ctx:gramaticaParser.ProgramContext):
        # La ptimera pasada recolecta TODAS las definiciones antes de validar CUALQUIER uso.
        
        # 1. Recolección de tareas (Definición y Etiquetas TAC)
        for item in ctx.getChildren():
            if isinstance(item, gramaticaParser.TaskContext):
                task_name = item.ID().getText()
                # Creamos etiquetas TAC descriptivas (ej: L_TAREA_inicio).
                task_label = f"L_TAREA_{task_name}" 
                self.symbol_table.define_task(task_name, item, task_label)

        # 2. Recolección de variables (Definición)
        for item in ctx.getChildren():
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

        # --- SEGUNDA PASADA: Validación y Generación de IR ---
        # En lugar de visitar TODOS los hijos (visitChildren), solo iteramos
        # sobre los nodos de TAREA. Cada tarea se encarga de visitar su propio contenido (statements)
        # y sus propias transiciones asociadas.
        for item in ctx.getChildren():
            if isinstance(item, gramaticaParser.TaskContext):
                self.visit(item) # Llama a visitTask
        
        return 

    def visitTask(self, ctx:gramaticaParser.TaskContext):
        task_name = ctx.ID().getText()
        task_label = self.symbol_table.get_task_label(task_name)
        
        # 1. Inicio de la Tarea en el TAC
        self.ir.add_instruction(op=f"{task_label}:") # Generamos la etiqueta TAC.
        
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
        
        # --- Generación del TAC para el Salto Condicional ---
        
        # 1. Evaluación de la condición (esto nos devuelve la temporal 'tN' que tiene True/False)
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
        
        # Traducción directa: TAC de asignación.
        self.ir.add_instruction(op='=', arg1=value, result=var_name)
        return

    def visitPrint_stmt(self, ctx:gramaticaParser.Print_stmtContext):
        value = ctx.VALUE().getText()
        
        # Traducción directa: TAC de impresión.
        self.ir.add_instruction(op='PRINT', arg1=value)
        return

    def visitCondition(self, ctx:gramaticaParser.ConditionContext):
        # 1. Verificación semántica: ¿La variable fue definida?
        var_name = ctx.ID().getText()
        self.symbol_table.check_variable_exists(var_name)
        
        op = ctx.comparator().getText()
        value = ctx.VALUE().getText()

        # 2. Generación del TAC para la comparación.
        temp_var = self.ir.new_temp() # Generamos la temporal para guardar el resultado True/False.
        
        # El TAC compara los valores y guarda el booleano en t1 (ej: t1 = estado == "OK").
        self.ir.add_instruction(op=op, arg1=var_name, arg2=value, result=temp_var)
        
        # Devolvemos la variable temporal para que visitTransition pueda usarla en el 'if_false_goto'.
        return temp_var