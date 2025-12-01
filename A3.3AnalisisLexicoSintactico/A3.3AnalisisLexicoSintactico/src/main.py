#!/usr/bin/env python3
"""
Validador de Reportes de Analisis de Sangre

Este programa valida archivos JSON que contienen reportes de analisis de
sangre, verificando:
1. Analisis lexico: tokens validos
2. Analisis sintactico: estructura JSON correcta
3. Analisis semantico: coherencia de campos, formatos y valores

Uso:
    python main.py <archivo.json>
    python main.py ruta/al/reporte.json
"""

import sys
import os
from parser import parse_text


def validar_reporte(filepath):
    """Valida un archivo JSON de reporte de analisis de sangre.

    Args:
        filepath: Ruta al archivo JSON a validar

    Muestra un reporte en consola con los resultados de la validacion.
    """
    print(f"Validando archivo: {os.path.basename(filepath)}")
    print("-" * 50)

    # Leer archivo
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"X Error: Archivo '{filepath}' no encontrado")
        return False
    except Exception as e:
        print(f"X Error al leer archivo: {e}")
        return False

    # Parsear y validar
    data, error = parse_text(text)

    if error:
        # Clasificar tipo de error
        if 'Error de sintaxis' in error:
            print("X Error sintactico:", error)
        elif 'Error de validacion' in error or 'Error semantico' in error:
            print("X Error semantico:", error.replace('Error de validacion: ', ''))
        elif 'Caracter invalido' in error:
            print("X Error lexico:", error)
        else:
            print("X Error:", error)

        print("\nArchivo INVALIDO")
        return False

    # Si llegamos aqui, el archivo es valido
    print("v Estructura general valida")
    print("v Fechas correctas")
    print("v Seccion 'Biometria Hematica' valida")
    print("v Todos los parametros son validos")
    print("v Formato de limites correcto")
    print("v Cedula profesional valida (8 digitos)")
    print("\nv Archivo verificado correctamente")

    return True


def main():
    """Funcion principal del programa."""
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.json>")
        print("\nEjemplo:")
        print("  python main.py reporte_hematologia.json")
        sys.exit(1)

    filepath = sys.argv[1]
    valido = validar_reporte(filepath)

    sys.exit(0 if valido else 1)


if __name__ == '__main__':
    main()