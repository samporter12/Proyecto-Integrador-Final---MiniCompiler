# Archivo: semantic_analyzer/SemanticAnalyzerVisitor.py
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
        if name in self.tasks:
            raise Exception(f"Error Semántico: Tarea '{name}' ya está definida.")
        self.tasks[name] = node
        self.task_labels[name] = label # Guardamos la etiqueta

    def define_variable(self, name, node):
        self.variables[name] = node

    def check_task_exists(self, name):
        if name not in self.tasks:
            raise Exception(f"Error Semántico: Intento de 'ir_a' a tarea no definida: '{name}'.")

    def check_variable_exists(self, name):
        if name not in self.variables:
            raise Exception(f"Error Semántico: Variable no definida '{name}' usada en condición.")

    def get_task_label(self, name):
        """Devuelve la etiqueta TAC para una tarea."""
        self.check_task_exists(name) # Validamos de paso
        return self.task_labels[name]


class SemanticAnalyzerVisitor(gramaticaVisitor):
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
                task_label = f"L_TAREA_{task_name}" 
                self.symbol_table.define_task(task_name, item, task_label)

        # 2. Recolectar variables
        for item in ctx.getChildren():
            # Si es una tarea, mira DENTRO de ella
            if isinstance(item, gramaticaParser.TaskContext):
                for stmt in item.statement():
                    if stmt.assignment_stmt():
                        var_name = stmt.assignment_stmt().ID().getText()
                        self.symbol_table.define_variable(var_name, stmt)
        
        # 3. Recolectar transiciones
        last_task_name = None
        temp_transitions = {}
        for item in ctx.getChildren():
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
        
        return # No devolvemos 'visitChildren'

    def visitTask(self, ctx:gramaticaParser.TaskContext):
        task_name = ctx.ID().getText()
        task_label = self.symbol_table.get_task_label(task_name)
        
        #  Generar TAC 
        self.ir.add_instruction(op=f"{task_label}:") # Etiqueta de inicio de tarea
        
        # Visita los statements (print, assign)
        self.visitChildren(ctx) 
        
        # Ahora, genera el TAC para las transiciones de ESTA tarea
        if task_name in self.task_transitions_map:
            for transition_node in self.task_transitions_map[task_name]:
                self.visit(transition_node) # Llama a visitTransition
        
        self.ir.add_instruction(op='RETURN') # Fin de la tarea
        self.ir.add_instruction(op='') # Línea en blanco para legibilidad
        return

    def visitTransition(self, ctx:gramaticaParser.TransitionContext):
        target_task_name = ctx.ID().getText()
        # Validamos y obtenemos la etiqueta de la tarea destino
        target_label = self.symbol_table.get_task_label(target_task_name)
        
        # Generar TAC 
        # 1. Visitar la condición, que devolverá el 'temp' (ej: t1)
        temp_var = self.visit(ctx.condition()) 
        
        # 2. Crear una etiqueta 'skip'
        skip_label = self.ir.new_label()
        
        # 3. Generar el salto condicional
        # if_false t1 goto L1
        self.ir.add_instruction(op='if_false_goto', arg1=temp_var, result=skip_label)
        
        # 4. Generar la llamada si la condición es VERDADERA
        # CALL L_TAREA_fin
        self.ir.add_instruction(op='CALL', result=target_label) 
        
        # 5. Generar la etiqueta 'skip'
        # L1:
        self.ir.add_instruction(op=f"{skip_label}:")
        return # No devolvemos nada, solo generamos IR

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
        # Valida: '... si [ID] == VALUE'
        var_name = ctx.ID().getText()
        self.symbol_table.check_variable_exists(var_name)
        
        op = ctx.comparator().getText()
        value = ctx.VALUE().getText()

        # Generar TAC 
        # 1. Generar una variable temporal para el resultado
        temp_var = self.ir.new_temp()
        
        # 2. t1 = estado == "OK"
        self.ir.add_instruction(op=op, arg1=var_name, arg2=value, result=temp_var)
        
        # 3. Devolver el nombre del temporal
        return temp_var