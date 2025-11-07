class IR:
    """
    Clase para almacenar la representación intermedia (TAC).
    Sigue el formato de 'visitor.ir.instructions' de tu ejemplo.
    """
    def __init__(self):
        self.instructions = [] # La lista principal donde se almacenan los diccionarios TAC.
        self.temp_counter = 0  # Contador usado para generar nombres de variables temporales (t1, t2, ...).
        self.label_counter = 0 # Contador usado para generar nombres de etiquetas de flujo (L1, L2, ...).

    def add_instruction(self, op, arg1=None, arg2=None, result=None):
        """Añade una instrucción TAC a la lista."""
        # Usamos un diccionario, ya que es la forma más flexible de representar
        # una instrucción de tres direcciones (operador, hasta dos argumentos, y un resultado).
        instruction = {
            'op': op,
            'arg1': arg1,
            'arg2': arg2,
            'result': result
        }
        self.instructions.append(instruction)
    
    def new_temp(self):
        """Genera un nuevo nombre de variable temporal (ej: t1, t2)."""
        # Es esencial para aislar el resultado de una expresión
        # antes de que se use en una instrucción de flujo
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self):
        """Genera un nuevo nombre de etiqueta (ej: L1, L2)."""
        # Se usa para marcar el punto a donde debe saltar el flujo de control
        self.label_counter += 1
        return f"L{self.label_counter}"

    def __str__(self):
        """Formatea las instrucciones para imprimirlas (como en tu ejemplo)."""
        # Este método es útil para la fase de depuración (mostrar el TAC en la consola).
        output = []
        for inst in self.instructions:
            op = inst['op']
            
            if op.endswith(':'): # Es una etiqueta
                # Las etiquetas (como L1: o L_TAREA_inicio:) se imprimen sin indentación.
                output.append(f"{op}")
            elif op == '=':
                output.append(f"    {inst['result']} = {inst['arg1']}")
            elif op == 'if_false_goto':
                # Esta es la instrucción clave para el flujo condicional ('ir_a').
                output.append(f"    if_false {inst['arg1']} goto {inst['result']}")
            elif op == 'goto':
                output.append(f"    goto {inst['result']}")
            elif op == 'PRINT':
                output.append(f"    PRINT {inst['arg1']}")
            elif op == 'CALL':
                # Simula la llamada a otra tarea (función) dentro del flujo.
                output.append(f"    CALL {inst['result']}")
            elif op == 'RETURN':
                # Marca el final lógico de una tarea.
                output.append(f"    RETURN")
            elif op in ['==', '!=', '>', '<', '>=', '<=']:
                # Instrucción para evaluar condiciones y almacenarlas en una temporal.
                output.append(f"    {inst['result']} = {inst['arg1']} {op} {inst['arg2']}")
            elif op == '':
                # Se usa para imprimir una línea en blanco y mejorar la legibilidad del TAC.
                output.append("") 
            else:
                 output.append(f"    {inst}") 
        
        return "\n".join(output)