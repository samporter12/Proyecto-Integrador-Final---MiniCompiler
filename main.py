# Archivo: main.py
import sys
import subprocess
from antlr4 import *

from generated.gramaticaLexer import gramaticaLexer
from generated.gramaticaParser import gramaticaParser
from semantic_analyzer.SemanticAnalyzerVisitor import SemanticAnalyzerVisitor
from codegen.PythonCodeGenerator import PythonCodeGenerator

def compile_source_code(source_code, job_index):
    """
    Función que toma un string de código fuente y lo compila,
    generando un archivo de salida único basado en el job_index.
    """
    
    print("\n" + "=" * 50)
    print(f"🚀 INICIANDO COMPILACIÓN (Trabajo #{job_index}) 🚀")
    print("=" * 50)

    # 1. Verificar si el código está vacío (ej. después de un split)
    if not source_code.strip():
        print("[INFO] Trabajo vacío, omitiendo.")
        return

    # 2. Fases 1 y 2: Léxico y Sintáctico
    # ¡Importante! Usamos InputStream(source_code) en lugar de FileStream
    try:
        input_stream = InputStream(source_code)
        lexer = gramaticaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = gramaticaParser(stream)
        
        print("Analizando sintaxis...")
        tree = parser.program() 
        print("[OK] Análisis Léxico y Sintáctico Exitoso.")
    except Exception as e:
        print(f"\n[ERROR] Error de Sintaxis Detectado (Trabajo #{job_index}):")
        print(e)
        return

    # 3. Fases 3 y 4: Semántico y Generación de IR
    print("\nIniciando Análisis Semántico y Generación de IR...")
    try:
        semantic_visitor = SemanticAnalyzerVisitor()
        semantic_visitor.visit(tree)
        
        print("[OK] Análisis Semántico Exitoso.")
        print("-" * 40)
        print("Tabla de Símbolos:")
        print(f"  Tareas: {list(semantic_visitor.symbol_table.tasks.keys())}")
        print(f"  Variables: {list(semantic_visitor.symbol_table.variables.keys())}")
        print("-" * 40)
        
        print("\nCódigo Intermedio (TAC):")
        print(semantic_visitor.ir)
        print("-" * 40)
        
    except Exception as e:
        print(f"\n[ERROR] Error Semántico Detectado (Trabajo #{job_index}):")
        print(e)
        return

    # 4. Fase 5: Generación de Código Final (Python)
    print("\nIniciando Generación de Código Final...")
    try:
        py_generator = PythonCodeGenerator(semantic_visitor.ir.instructions)
        python_code = py_generator.generate()
        
        # Generar nombre de archivo único
        output_filename = f"output_program_{job_index}.py"
        
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(python_code)
        print(f"[OK] Código Python generado y guardado en: {output_filename}")
        
    except Exception as e:
        print(f"\n[ERROR] No se pudo escribir el archivo de salida (Trabajo #{job_index}): {e}")
        return

    # 5. Fase 6: Ejecución del script generado
    print(f"\nEjecutando {output_filename}...")
    try:
        result = subprocess.run(
            [sys.executable, output_filename],
            capture_output=True, text=True, check=True
        )
        print("--- SALIDA DEL SCRIPT ---")
        print(result.stdout.strip())
        print("-------------------------")
        if result.stderr:
            print("--- Errores de Ejecución ---")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] El script (Trabajo #{job_index}) falló al ejecutarse.")
        print(e.stdout)
        print(e.stderr)
    except Exception as e:
        print(f"\n[ERROR] No se pudo ejecutar el script (Trabajo #{job_index}): {e}")


def main():
    """
    Punto de entrada principal. Lee el input.txt, lo divide
    y llama al compilador para cada parte.
    """
    input_filename = "input.txt"
    separator = "---NUEVO_TRABAJO---"
    
    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{input_filename}'")
        return
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        return

    # Dividir el contenido del archivo por el separador
    jobs = file_content.split(separator)
    
    print(f"✅ Se encontraron {len(jobs)} trabajos en '{input_filename}'.")
    
    # Iterar y compilar cada trabajo
    for i, job_code in enumerate(jobs):
        compile_source_code(job_code, i + 1)
        
    print("\n" + "=" * 50)
    print("¡COMPILACIÓN DE TODOS LOS TRABAJOS FINALIZADA!")
    print("=" * 50)

if __name__ == '__main__':
    main()