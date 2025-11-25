r"""
Analizador sintáctico (parser) usando PLY para una versión reducida de JSON.

Este parser construye un diccionario Python a partir de un objeto JSON reducido
y luego ejecuta una validación semántica para asegurar la presencia y tipo de
los campos requeridos:

Estructura esperada (ejemplo):
{
  "folio": 15502427,
  "fecha_toma": "14/06/2020 07:51:57",
  "fecha_validacion": "14/06/2020 17:08:05",
  "paciente": {
    "nombre": "Ramírez Guzmán, María",
    "fecha_nacimiento": "25/04/1985",
    "sexo": "F",
    "edad": 35
  }
}

Funciones exportadas:
- parse_text(text): devuelve (data, None) si parse y validación OK, o (None, mensaje_error).
- build_parser(): construye el parser PLY.

Comentarios en español explican las reglas sintácticas definidas.
"""

import re
import ply.yacc as yacc
from lexer import tokens, build_lexer

# ------ Reglas de la gramática (sintaxis) ------

def p_start(t):
    'start : object'
    t[0] = t[1]

def p_object_empty(t):
    'object : LBRACE RBRACE'
    t[0] = {}

def p_object_members(t):
    'object : LBRACE members RBRACE'
    # members es una lista de pares (clave, valor)
    t[0] = dict(t[2])

def p_members_single(t):
    'members : pair'
    t[0] = [t[1]]

def p_members_multiple(t):
    'members : members COMMA pair'
    t[0] = t[1] + [t[3]]

def p_pair(t):
    'pair : STRING COLON value'
    t[0] = (t[1], t[3])

def p_value_string(t):
    'value : STRING'
    t[0] = t[1]

def p_value_number(t):
    'value : NUMBER'
    t[0] = t[1]

def p_value_object(t):
    'value : object'
    t[0] = t[1]

def p_error(t):
    if t is None:
        raise SyntaxError('Error de sintaxis: fin de entrada inesperado')
    else:
        raise SyntaxError(f"Error de sintaxis en token '{t.value}' (tipo {t.type})")


def build_parser(**kwargs):
    r"""Construye y devuelve el parser PLY."""
    import sys
    return yacc.yacc(module=sys.modules[__name__], **kwargs)


# ------ Validación semántica de la estructura específica ------

date_time_re = re.compile(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$')
date_re = re.compile(r'^\d{2}/\d{2}/\d{4}$')

def validate_structure(data):
    r"""Valida que el dict `data` cumpla con la estructura requerida.

    Devuelve (True, None) si OK o (False, mensaje_error) en caso contrario.
    """
    if not isinstance(data, dict):
        return False, 'La raíz no es un objeto JSON'

    required_top = ['folio', 'fecha_toma', 'fecha_validacion', 'paciente']
    for k in required_top:
        if k not in data:
            return False, f"Falta campo requerido en raíz: '{k}'"

    # folio debe ser entero
    if not isinstance(data['folio'], int):
        return False, "El campo 'folio' debe ser un número entero"

    # fechas con formato 'dd/mm/yyyy HH:MM:SS'
    if not isinstance(data['fecha_toma'], str) or not date_time_re.match(data['fecha_toma']):
        return False, "El campo 'fecha_toma' debe ser una cadena con formato 'dd/mm/yyyy HH:MM:SS'"
    if not isinstance(data['fecha_validacion'], str) or not date_time_re.match(data['fecha_validacion']):
        return False, "El campo 'fecha_validacion' debe ser una cadena con formato 'dd/mm/yyyy HH:MM:SS'"

    paciente = data['paciente']
    if not isinstance(paciente, dict):
        return False, "El campo 'paciente' debe ser un objeto"

    required_p = ['nombre', 'fecha_nacimiento', 'sexo', 'edad']
    for k in required_p:
        if k not in paciente:
            return False, f"Falta campo en 'paciente': '{k}'"

    if not isinstance(paciente['nombre'], str):
        return False, "'paciente.nombre' debe ser una cadena"
    if not isinstance(paciente['fecha_nacimiento'], str) or not date_re.match(paciente['fecha_nacimiento']):
        return False, "'paciente.fecha_nacimiento' debe tener formato 'dd/mm/yyyy'"
    if not isinstance(paciente['sexo'], str) or len(paciente['sexo']) not in (1,):
        return False, "'paciente.sexo' debe ser un carácter (ej. 'M' o 'F')"
    if not isinstance(paciente['edad'], int):
        return False, "'paciente.edad' debe ser un número entero"

    return True, None


def parse_text(text):
    r"""Parsea `text` y valida la estructura.

    Devuelve (data, None) si OK, o (None, mensaje_error) en caso de falla.
    """
    lexer = build_lexer()
    parser = build_parser()
    try:
        data = parser.parse(text, lexer=lexer)
    except SyntaxError as e:
        return None, f'Error de sintaxis: {e}'
    except Exception as e:
        return None, f'Error al parsear: {e}'

    ok, msg = validate_structure(data)
    if not ok:
        return None, f'Error de validación: {msg}'

    return data, None


if __name__ == '__main__':
    # Modo prueba: lee desde stdin y muestra el resultado
    import sys
    text = sys.stdin.read()
    if not text.strip():
        text = '''{
  "folio": 15502427,
  "fecha_toma": "14/06/2020 07:51:57",
  "fecha_validacion": "14/06/2020 17:08:05",
  "paciente": {
    "nombre": "Ramírez Guzmán, María",
    "fecha_nacimiento": "25/04/1985",
    "sexo": "F",
    "edad": 35
  }
}'''

    data, err = parse_text(text)
    if err:
        print('INVALID:', err)
    else:
        print('VALID: objeto parseado correctamente')
        import json
        print(json.dumps(data, ensure_ascii=False, indent=2))
