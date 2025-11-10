class PythonCodeGenerator:
    """
    Clase que implementa la Fase 5 del compilador.
    Traduce la lista de instrucciones TAC (Código de Tres Direcciones)
    a un script de Python (.py) completamente funcional.
    """
    def __init__(self, tac_instructions):
        self.tac = tac_instructions
        self.python_code = []     # Lista donde almacenaremos cada línea del script final.
        self.indent_level = 0     # Controla el nivel de indentación (necesario para la sintaxis de Python).
        self.variables = set()    # Usaremos un conjunto para recolectar todas las variables únicas (incluyendo temporales)
                                  # y poder declararlas como globales al inicio.

    # --- Métodos de Control de Formato ---

    def emit(self, line):
        """Añade una línea de código con la indentación correcta (4 espacios por nivel)."""
        indent = "    " * self.indent_level
        self.python_code.append(indent + line)

    def indent(self):
        """Aumenta el nivel de indentación (ej: después de 'def' o 'if')."""
        self.indent_level += 1

    def dedent(self):
        """Disminuye el nivel de indentación (ej: después de 'return' o al llegar a una etiqueta 'L1:')."""
        if self.indent_level > 0:
            self.indent_level -= 1

    # --- Métodos de Pre-procesamiento ---

    def collect_variables(self):
        """
        Recorre el TAC para identificar todas las variables y temporales utilizadas
        y las añade al conjunto 'self.variables'. Esto es necesario para:
        1. Declararlas e inicializarlas como variables globales en el script Python.
        2. Usar 'global variable_name' dentro de cada función.
        """
        for inst in self.tac:
            # Recolectar variables de asignaciones directas (resultado)
            if inst['op'] == '=':
                self.variables.add(inst['result'])
            # Recolectar variables de comparaciones (argumento 1 y resultado temporal)
            if inst['op'] in ['==', '!=', '>', '<', '>=', '<=']:
                self.variables.add(inst['arg1'])
                self.variables.add(inst['result']) # Las temporales (t1, t2)
            # Recolectar variables usadas como condición en saltos
            if inst['op'] == 'if_false_goto':
                self.variables.add(inst['arg1'])

    # --- Lógica Principal de Generación ---

    def generate(self):
        """
        Método principal que orquesta la generación del script Python completo.
        """
        self.emit("# --- Código Python Generado Automáticamente ---")
        self.emit("")
        
        # 1. Declarar variables globales e inicializarlas (Paso obligatorio para Python).
        self.collect_variables()
        self.emit("# --- Declaración de Variables Globales ---")
        for var in sorted(list(self.variables)):
            # Inicializamos todas las variables a None para evitar errores de Scope/Referencia.
            self.emit(f"{var} = None") 
        self.emit("")

        # 2. Traducir el TAC instrucción por instrucción.
        self.emit("# --- Definición de Tareas (Funciones) ---")
        for inst in self.tac:
            self.translate_instruction(inst)
        
        # 3. Añadir el punto de entrada (el 'main' del script).
        self.emit("")
        self.emit("# --- Punto de Entrada ---")
        self.emit("if __name__ == '__main__':")
        self.indent()
        
        # Encontramos la primera tarea para saber dónde iniciar el flujo.
        first_task_label = self.find_first_task_label()
        if first_task_label:
            # Convertimos la etiqueta TAC (L_TAREA_inicio) al nombre de la función (inicio).
            func_name = first_task_label.replace("L_TAREA_", "")
            self.emit(f"print('--- Iniciando Flujo de Trabajo ---')")
            self.emit(f"{func_name}()") # Llamamos a la primera tarea para arrancar el programa.
            self.emit(f"print('--- Flujo de Trabajo Terminado ---')")
        else:
            self.emit("print('Error: No se encontró una tarea inicial.')")
        self.dedent()
        
        return "\n".join(self.python_code) # Devolvemos el script final como una sola cadena de texto.

    def find_first_task_label(self):
        """Busca la primera instrucción que sea una etiqueta de tarea (L_TAREA_...)."""
        for inst in self.tac:
            if inst['op'].startswith('L_TAREA_'):
                return inst['op'][:-1] # Devolvemos la etiqueta sin los dos puntos (:)
        return None

    # --- Traducción de Instrucciones TAC ---

    def translate_instruction(self, inst):
        """Traduce una sola instrucción TAC a Python."""
        op = inst['op']

        if op.startswith('L_TAREA_'):
            # El inicio de una tarea TAC se traduce a una definición de función Python.
            func_name = op.replace("L_TAREA_", "")[:-1] 
            self.emit("") 
            self.emit(f"def {func_name}():")
            self.indent()
            # Es vital declarar las variables globales aquí para que la función pueda modificarlas.
            for var in self.variables:
                self.emit(f"global {var}")
            
        elif op == 'RETURN':
            # El fin de la lógica de la tarea se traduce a 'return'.
            self.emit("return")
            self.dedent() # Cerramos el bloque 'def' de la función.
        
        elif op.startswith('L') and op.endswith(':'):
            # Esta es una etiqueta de salto generada por el compilador (ej: L1:).
            # En Python, manejamos el flujo de control con indentación, no con GOTO/Etiquetas.
            self.dedent() # Cerramos el bloque 'if' que se abrió con 'if_false_goto'.
            self.emit(f"# Etiqueta {op} (manejada por indentación)")
            
        elif op == '=':
            # Asignación directa. Traducción 1:1.
            self.emit(f"{inst['result']} = {inst['arg1']}")
            
        elif op == 'PRINT':
            # Impresión de valores. Traducción 1:1.
            self.emit(f"print({inst['arg1']})")
            
        elif op in ['==', '!=', '>', '<', '>=', '<=']:
            # Asignación del resultado de una comparación a una variable temporal. Traducción 1:1.
            self.emit(f"{inst['result']} = {inst['arg1']} {op} {inst['arg2']}")
            
        elif op == 'if_false_goto':
            # Esta instrucción TAC (salta si es FALSO) se convierte a un bloque IF.
            # Convertimos: "si NO t1 salta a L1" a "si t1 es VERDADERO, ejecuta el bloque".
            self.emit(f"if {inst['arg1']}:")
            self.indent() # Abrimos un nuevo nivel de indentación para el bloque IF.
            # El CALL (la siguiente instrucción) se imprimirá dentro de este 'if'.
        
        elif op == 'CALL':
            # La llamada a la tarea destino (salto) se traduce a una llamada de función Python.
            func_name = inst['result'].replace("L_TAREA_", "")
            self.emit(f"{func_name}()")
            
        elif op == 'goto':
            # (No se usa en este DSL, pero se comenta por si fuera necesario).
            self.emit(f"# goto {inst['result']} (no implementado)")
            
        elif op == '':
            # Línea vacía que agregamos al final de cada tarea en el TAC para legibilidad.
            pass