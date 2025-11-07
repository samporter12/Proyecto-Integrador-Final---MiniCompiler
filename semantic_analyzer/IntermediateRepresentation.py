# Archivo: semantic_analyzer/IntermediateRepresentation.py

class IR:
    """
    Clase para almacenar la representación intermedia (TAC).
    Sigue el formato de 'visitor.ir.instructions' de tu ejemplo.
    """
    def __init__(self):
        self.instructions = [] # La lista de instrucciones TAC
        self.temp_counter = 0
        self.label_counter = 0

    def add_instruction(self, op, arg1=None, arg2=None, result=None):
        """Añade una instrucción TAC a la lista."""
        # Usamos un diccionario, igual que en tu ejemplo de IfElseLang
        instruction = {
            'op': op,
            'arg1': arg1,
            'arg2': arg2,
            'result': result
        }
        self.instructions.append(instruction)
    
    def new_temp(self):
        """Genera un nuevo nombre de variable temporal (ej: t1, t2)."""
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self):
        """Genera un nuevo nombre de etiqueta (ej: L1, L2)."""
        self.label_counter += 1
        return f"L{self.label_counter}"

    def __str__(self):
        """Formatea las instrucciones para imprimirlas."""
        output = []
        for inst in self.instructions:
            op = inst['op']
            
            if op.endswith(':'): # Es una etiqueta
                output.append(f"{op}")
            elif op == '=':
                output.append(f"    {inst['result']} = {inst['arg1']}")
            elif op == 'if_false_goto':
                output.append(f"    if_false {inst['arg1']} goto {inst['result']}")
            elif op == 'goto':
                output.append(f"    goto {inst['result']}")
            elif op == 'PRINT':
                output.append(f"    PRINT {inst['arg1']}")
            elif op == 'CALL':
                output.append(f"    CALL {inst['result']}")
            elif op == 'RETURN':
                output.append(f"    RETURN")
            elif op in ['==', '!=', '>', '<', '>=', '<=']:
                output.append(f"    {inst['result']} = {inst['arg1']} {op} {inst['arg2']}")
            elif op == '':
                output.append("") # Imprime una línea vacía
            else:
                 output.append(f"    {inst}") # genérico
        
        return "\n".join(output)