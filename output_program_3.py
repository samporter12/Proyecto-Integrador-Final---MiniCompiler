# --- Código Python Generado Automáticamente ---

# --- Declaración de Variables Globales ---
t1 = None
variable_B = None

# --- Definición de Tareas (Funciones) ---

def Chequeo():
    global variable_B
    global t1
    print("Iniciando Flujo 3")
    variable_B = "PENDIENTE"
    t1 = variable_B == "PENDIENTE"
    if t1:
        Exito()
    # Etiqueta L1: (manejada por indentación)
    return

def Exito():
    global variable_B
    global t1
    print("Flujo 3 Exitoso")
    return

# --- Punto de Entrada ---
if __name__ == '__main__':
    print('--- Iniciando Flujo de Trabajo ---')
    Chequeo()
    print('--- Flujo de Trabajo Terminado ---')