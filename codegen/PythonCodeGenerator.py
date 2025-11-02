# Archivo: codegen/PythonCodeGenerator.py

class PythonCodeGenerator:
    """
    Traduce la lista de instrucciones TAC (diccionarios) a un script de Python.
    """
    def __init__(self, tac_instructions):
        self.tac = tac_instructions
        self.python_code = [] # Lista para guardar las líneas de código Python
        self.indent_level = 0
        self.variables = set() # Para declarar variables globales

    def emit(self, line):
        """Añade una línea de código con la indentación correcta."""
        indent = "    " * self.indent_level
        self.python_code.append(indent + line)

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        if self.indent_level > 0:
            self.indent_level -= 1

    def collect_variables(self):
        """
        Pasa por el TAC para encontrar todas las variables
        y declararlas al inicio del script.
        """
        for inst in self.tac:
            # Variables usadas en asignaciones (ej: estado = "OK")
            if inst['op'] == '=':
                self.variables.add(inst['result'])
            # Variables usadas en condiciones (ej: t1 = estado == "OK")
            if inst['op'] in ['==', '!=', '>', '<', '>=', '<=']:
                self.variables.add(inst['arg1'])
                self.variables.add(inst['result']) # Las temporales
            # Variables en if_false_goto (ej: if_false t1 ...)
            if inst['op'] == 'if_false_goto':
                self.variables.add(inst['arg1'])

    def generate(self):
        """
        Método principal que genera todo el script de Python.
        """
        self.emit("# --- Código Python Generado Automáticamente ---")
        self.emit("")
        
        # 1. Declarar todas las variables como globales
        self.collect_variables()
        self.emit("# --- Declaración de Variables Globales ---")
        for var in sorted(list(self.variables)):
            # Inicializamos todo a None (o 0)
            self.emit(f"{var} = None") 
        self.emit("")

        # 2. Traducir cada instrucción TAC
        self.emit("# --- Definición de Tareas (Funciones) ---")
        for inst in self.tac:
            self.translate_instruction(inst)
        
        # 3. Añadir el punto de entrada
        self.emit("")
        self.emit("# --- Punto de Entrada ---")
        self.emit("if __name__ == '__main__':")
        self.indent()
        # Asumimos que la primera tarea es el inicio
        first_task_label = self.find_first_task_label()
        if first_task_label:
            # Convertimos "L_TAREA_inicio" a "inicio()"
            func_name = first_task_label.replace("L_TAREA_", "")
            self.emit(f"print('--- Iniciando Flujo de Trabajo ---')")
            self.emit(f"{func_name}()") # Llama a la primera tarea
            self.emit(f"print('--- Flujo de Trabajo Terminado ---')")
        else:
            self.emit("print('Error: No se encontró una tarea inicial.')")
        self.dedent()
        
        return "\n".join(self.python_code)

    def find_first_task_label(self):
        """Encuentra la primera etiqueta de TAREA en el TAC."""
        for inst in self.tac:
            if inst['op'].startswith('L_TAREA_'):
                return inst['op'][:-1] # Devuelve "L_TAREA_inicio"
        return None

    def translate_instruction(self, inst):
        """Traduce una sola instrucción TAC a Python."""
        op = inst['op']

        if op.startswith('L_TAREA_'):
            # TAC: L_TAREA_inicio:
            # Python: def inicio():
            func_name = op.replace("L_TAREA_", "")[:-1] # Quita "L_TAREA_" y ":"
            self.emit("") # Línea en blanco
            self.emit(f"def {func_name}():")
            self.indent()
            # Declarar que vamos a usar las variables globales
            for var in self.variables:
                self.emit(f"global {var}")
            
        elif op == 'RETURN':
            # TAC: RETURN
            # Python: return
            self.emit("return")
            self.dedent() # Salimos de la función 'def'
        
        elif op.startswith('L') and op.endswith(':'):
            # TAC: L1:
            # Python: (Manejo de indentación)
            # Las etiquetas en Python no existen, se manejan con 'if/else'.
            # Necesitamos bajar la indentación que subimos en 'if_false_goto'.
            self.dedent()
            self.emit(f"# Etiqueta {op} (manejada por indentación)")
            
        elif op == '=':
            # TAC: estado = "OK"
            # Python: estado = "OK"
            self.emit(f"{inst['result']} = {inst['arg1']}")
            
        elif op == 'PRINT':
            # TAC: PRINT "Comenzando"
            # Python: print("Comenzando")
            self.emit(f"print({inst['arg1']})")
            
        elif op in ['==', '!=', '>', '<', '>=', '<=']:
            # TAC: t1 = estado == "OK"
            # Python: t1 = estado == "OK"
            self.emit(f"{inst['result']} = {inst['arg1']} {op} {inst['arg2']}")
            
        elif op == 'if_false_goto':
            # TAC: if_false t1 goto L1
            # Python: if t1:
            #             ... (codigo)
            #         # L1:
            self.emit(f"if {inst['arg1']}:")
            self.indent()
            # El código que sigue (el CALL) se indentará aquí dentro.
            # Cuando llegue la etiqueta 'L1:', haremos un dedent().
        
        elif op == 'CALL':
            # TAC: CALL L_TAREA_fin
            # Python: fin()
            func_name = inst['result'].replace("L_TAREA_", "")
            self.emit(f"{func_name}()")
            
        elif op == 'goto':
            # No lo usamos en este lenguaje, pero si lo hiciéramos:
            self.emit(f"# goto {inst['result']} (no implementado)")
            
        elif op == '':
            # Línea vacía para legibilidad
            pass