import sys
import subprocess 
from antlr4 import *

from generated.gramaticaLexer import gramaticaLexer
from generated.gramaticaParser import gramaticaParser

from semantic_analyzer.SemanticAnalyzerVisitor import SemanticAnalyzerVisitor
from codegen.PythonCodeGenerator import PythonCodeGenerator

def compile_source_code(source_code, job_index):
    """
    Función que encapsula todo el pipeline de compilación para un único trabajo (Job).
    Esto nos permite procesar varios flujos de trabajo de forma independiente.
    """
    
    print("\n" + "=" * 50)
    print(f"🚀 INICIANDO COMPILACIÓN (Trabajo #{job_index}) 🚀")
    print("=" * 50)

    # 1. Verificación preliminar (para saltar bloques vacíos después del split)
    if not source_code.strip():
        print("[INFO] Trabajo vacío, omitiendo.")
        return

    # 2. Fases 1 y 2: Análisis Léxico y Sintáctico
    try:
        input_stream = InputStream(source_code)
        lexer = gramaticaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = gramaticaParser(stream)
        
        print("Analizando sintaxis...")
        tree = parser.program() # Construye el Parse Tree (CST).
        print("[OK] Análisis Léxico y Sintáctico Exitoso.")
    except Exception as e:
        # Si falla el try, capturamos el ERROR DE SINTAXIS y detenemos el trabajo.
        print(f"\n[ERROR] Error de Sintaxis Detectado (Trabajo #{job_index}):")
        print(e)
        return

    # 3. Fases 3 y 4: Análisis Semántico y Generación de Código Intermedio (IR)
    print("\nIniciando Análisis Semántico y Generación de IR...")
    try:
        semantic_visitor = SemanticAnalyzerVisitor()
        semantic_visitor.visit(tree) 
        
        print("[OK] Análisis Semántico Exitoso.")
        
        # Reportamos el resultado de la Fase 3 (Tabla de Símbolos).
        print("-" * 40)
        print("Tabla de Símbolos:")
        print(f"  Tareas: {list(semantic_visitor.symbol_table.tasks.keys())}")
        print(f"  Variables: {list(semantic_visitor.symbol_table.variables.keys())}")
        print("-" * 40)
        
        # Reportamos el resultado de la Fase 4 (Código Intermedio TAC).
        print("\nCódigo Intermedio (TAC):")
        print(semantic_visitor.ir)
        print("-" * 40)
        
    except Exception as e:
        # Si falla el try, capturamos el ERROR SEMÁNTICO (ej: tarea no definida) y detenemos el trabajo.
        print(f"\n[ERROR] Error Semántico Detectado (Trabajo #{job_index}):")
        print(e)
        return

    # 4. Fase 5: Generación de Código Final (Python)
    print("\nIniciando Generación de Código Final...")
    try:
        # Creamos el generador pasando nuestra lista de instrucciones TAC.
        py_generator = PythonCodeGenerator(semantic_visitor.ir.instructions)
        python_code = py_generator.generate()
        
        # Asignamos un nombre único al archivo de salida para cada trabajo.
        output_filename = f"output_program_{job_index}.py"
        
        # Escribimos el script Python generado al disco.
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(python_code)
        print(f"[OK] Código Python generado y guardado en: {output_filename}")
        
    except Exception as e:
        # Manejo de errores de escritura.
        print(f"\n[ERROR] No se pudo escribir el archivo de salida (Trabajo #{job_index}): {e}")
        return

    # 5. Fase 6: Ejecución del script generado (Prueba de Fuego)
    print(f"\nEjecutando {output_filename}...")
    try:
        # Usamos subprocess.run para ejecutar el archivo .py con el intérprete de Python del sistema.
        # Esto verifica que el código generado sea realmente ejecutable.
        result = subprocess.run(
            [sys.executable, output_filename],
            capture_output=True, text=True, check=True
        )
        print("--- SALIDA DEL SCRIPT ---")
        print(result.stdout.strip()) # Imprimimos lo que el script compilado hizo.
        print("-------------------------")
        
    except subprocess.CalledProcessError as e:
        # Si el script Python generado tiene un error en tiempo de ejecución.
        print(f"\n[ERROR] El script (Trabajo #{job_index}) falló al ejecutarse.")
        print(e.stdout)
        print(e.stderr)
    except Exception as e:
        # Otros errores de ejecución.
        print(f"\n[ERROR] No se pudo ejecutar el script (Trabajo #{job_index}): {e}")


def main():
    """
    Punto de entrada principal. Se encarga de la lectura del archivo de entrada
    y de la separación de los trabajos.
    """
    input_filename = "input.txt"
    separator = "---NUEVO_TRABAJO---" # Nuestro delimitador customizado.
    
    # Lectura del archivo de entrada completo
    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{input_filename}'")
        return
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        return

    # Dividir el contenido del archivo por el separador customizado.
    jobs = file_content.split(separator)
    
    print(f"✅ Se encontraron {len(jobs)} trabajos en '{input_filename}'.")
    
    # Iterar y llamar a la función de compilación para cada bloque.
    for i, job_code in enumerate(jobs):
        compile_source_code(job_code, i + 1)
        
    print("\n" + "=" * 50)
    print("¡COMPILACIÓN DE TODOS LOS TRABAJOS FINALIZADA!")
    print("=" * 50)

if __name__ == '__main__':
    main()