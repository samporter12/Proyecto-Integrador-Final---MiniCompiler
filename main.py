import sys  
import os 
import subprocess
from antlr4 import *

from generated.gramaticaLexer import gramaticaLexer
from generated.gramaticaParser import gramaticaParser

from semantic_analyzer.SemanticAnalyzerVisitor import SemanticAnalyzerVisitor
from codegen.PythonCodeGenerator import PythonCodeGenerator

def main():
    # PASO 1: Validar la entrada del usuario 
    if len(sys.argv) != 2:
        print("Error: Debes proporcionar el nombre del archivo de entrada.")
        print("Uso: python main.py <nombre_archivo.txt>")
        return 
    
    input_filename = sys.argv[1] # El nombre del archivo (ej: 'flujo_1.txt')

    # PASO 2: Definir el nombre del archivo de salida
    base_name = os.path.basename(input_filename) 
    name_without_ext = os.path.splitext(base_name)[0] 
    output_filename = f"output_{name_without_ext}.py"
    
    print("=" * 50)
    print(f"🚀 INICIANDO COMPILADOR 🚀")
    print(f"  Archivo de Entrada: {input_filename}")
    print(f"  Archivo de Salida:  {output_filename}")
    print("=" * 50)

    # FASE 1: Cargar archivo y Análisis Léxico 
    try:
        input_stream = FileStream(input_filename, encoding='utf-8')
        lexer = gramaticaLexer(input_stream)
        stream = CommonTokenStream(lexer)
    except FileNotFoundError:
        print(f"\n[ERROR] No se encontró el archivo: {input_filename}")
        return
    except Exception as e:
        print(f"\n[ERROR] Cargando archivo: {e}")
        return

    # FASE 2: Análisis Sintáctico 
    try:
        parser = gramaticaParser(stream)
        tree = parser.program() 
        print("\n[OK] Fase 1/2: Análisis Léxico y Sintáctico Exitoso.")

        print("\n--- 🌳 Árbol Sintáctico (Parse Tree) 🌳 ---")
        # El 'recog=parser' muestra el nombre de las reglas
        print(tree.toStringTree(recog=parser))
        print("---------------------------------------------")

    except Exception as e:
        print(f"\n[ERROR] Error de Sintaxis Detectado:")
        print(e)
        return

    # FASES 3/4: Análisis Semántico y Generación de IR (TAC) 
    print("\nIniciando Fases 3 y 4 (Semántica y TAC)...")
    try:
        semantic_visitor = SemanticAnalyzerVisitor()
        semantic_visitor.visit(tree) 
        
        print("[OK] Análisis Semántico Exitoso.")
        
        # Reportamos el resultado de la Fase 3
        print("-" * 40)
        print("Tabla de Símbolos:")
        print(f"  Tareas: {list(semantic_visitor.symbol_table.tasks.keys())}")
        print(f"  Variables: {list(semantic_visitor.symbol_table.variables.keys())}")
        print("-" * 40)
        
        # Reportamos el resultado de la Fase 4 
        print("\nCódigo Intermedio (TAC):")
        print(semantic_visitor.ir)
        print("-" * 40)
        
    except Exception as e:
        print(f"\n[ERROR] Error Semántico Detectado:")
        print(e)
        return

    # FASE 5: Generación de Código Final
    print("\nIniciando Fase 5 (Generación de Código Python)...")
    try:
        # Creamos el generador pasando nuestra lista de instrucciones TAC.
        py_generator = PythonCodeGenerator(semantic_visitor.ir.instructions)
        python_code = py_generator.generate()
        
        # Escribimos el script Python generado al disco.
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(python_code)
        print(f"[OK] Código Python generado y guardado en: {output_filename}")
        
    except Exception as e:
        print(f"\n[ERROR] No se pudo escribir el archivo de salida: {e}")
        return

    # FASE 6: Ejecución del script generado 
    print("\nIniciando Fase 6 (Ejecución)...")
    try:
        result = subprocess.run(
            [sys.executable, output_filename],
            capture_output=True, text=True, check=True
        )
        print("--- SALIDA DEL SCRIPT ---")
        print(result.stdout.strip()) # Imprimimos lo que el script compilado hizo.
        print("-------------------------")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] El script falló al ejecutarse.")
        print(e.stdout)
        print(e.stderr)
    except Exception as e:
        print(f"\n[ERROR] No se pudo ejecutar el script: {e}")

    print("\n" + "=" * 50)
    print("¡COMPILACIÓN FINALIZADA!")
    print("=" * 50)


if __name__ == '__main__':
    main()