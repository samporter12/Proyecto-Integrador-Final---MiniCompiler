# --- Código Python Generado Automáticamente ---

# --- Declaración de Variables Globales ---
estado = None
t1 = None

# --- Definición de Tareas (Funciones) ---

def inicio():
    global estado
    global t1
    print("Comenzando Flujo 1")
    estado = "OK"
    t1 = estado == "OK"
    if t1:
        fin()
    # Etiqueta L1: (manejada por indentación)
    return

def fin():
    global estado
    global t1
    print("Terminado Flujo 1")
    return

# --- Punto de Entrada ---
if __name__ == '__main__':
    print('--- Iniciando Flujo de Trabajo ---')
    inicio()
    print('--- Flujo de Trabajo Terminado ---')