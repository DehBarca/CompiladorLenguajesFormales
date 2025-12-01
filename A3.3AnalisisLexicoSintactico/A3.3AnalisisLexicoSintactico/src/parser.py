r"""
Este módulo usa PLY (y el lexer definido en `src/lexer.py`) para definir
una gramática libre de contexto (GLC) que reconoce objetos JSON Completos
incluyendo arrays, necesarios para validar reportes de analisis de sangre. Tras parsear, el módulo realiza una
validación semántica específica para el esquema requerido por la práctica
(campos `folio`, `fecha_toma`, `paciente`, ...).

Funciones principales exportadas:
- `parse_text(text)`: parsea el texto y devuelve `(data, None)` si es válido
    o `(None, mensaje_error)` si hay fallo de sintaxis/validación.
- `build_parser()`: construye el parser PLY (útil para pruebas o uso directo).
"""

import re
import ply.yacc as yacc
from lexer import tokens, build_lexer

# ------ Reglas de la gramática (sintaxis) ------
def p_start(t):
    '''start : object'''
    """Producción inicial.

    start -> object
    Devuelve directamente el objeto parseado como diccionario.
    """
    t[0] = t[1]

def p_object_empty(t):
    '''object : LBRACE RBRACE'''
    """Objeto vacío.

    object -> { }
    Se mapea a un diccionario vacío.
    """
    t[0] = {}

def p_object_members(t):
    '''object : LBRACE members RBRACE'''
    """Objeto con miembros (pares clave-valor).

    object -> { members }
    `members` se construye como una lista de tuplas (clave, valor),
    por eso se convierte a `dict` para obtener un mapeo Python.
    """
    # members es una lista de pares (clave, valor)
    t[0] = dict(t[2])

def p_members_single(t):
    '''members : pair'''
    """Lista de miembros con un único par."""
    t[0] = [t[1]]

def p_members_multiple(t):
    '''members : members COMMA pair'''
    """Lista de miembros extendida por coma.

    Permite construir una lista acumulativa de pares.
    """
    t[0] = t[1] + [t[3]]

def p_pair(t):
    '''pair : STRING COLON value'''
    """Par clave-valor.

    pair -> STRING : value
    Retorna una tupla (clave, valor) que luego se usará para construir
    el diccionario del objeto.
    """
    t[0] = (t[1], t[3])

def p_value_string(t):
    '''value : STRING'''
    """Valor tipo cadena."""
    t[0] = t[1]

def p_value_number(t):
    '''value : NUMBER'''
    """Valor tipo número entero."""
    t[0] = t[1]

def p_value_object(t):
    '''value : object'''
    """Valor que es a su vez un objeto (anidamiento)."""
    t[0] = t[1]

def p_value_array(t):
    '''value : array'''
    """Valor que es un array (lista)."""
    t[0] = t[1]

def p_array_empty(t):
    '''array : LBRACKET RBRACKET'''
    t[0] = []

def p_array_elements(t):
    '''array : LBRACKET elements RBRACKET'''
    t[0] = t[2]

def p_elements_single(t):
    '''elements : value'''
    t[0] = [t[1]]

def p_elements_multiple(t):
    '''elements : elements COMMA value'''
    t[0] = t[1] + [t[3]]

def p_error(t):
    """Manejador de errores sintácticos del parser.

    - Si `t` es `None`, significa que la entrada terminó inesperadamente.
    - En caso contrario se informa el token que causó el fallo.
    PLY llamará a esta función en caso de error durante el parseo.
    """
    if t is None:
        raise SyntaxError('Error de sintaxis: fin de entrada inesperado')
    else:
        raise SyntaxError(f"Error de sintaxis en token '{t.value}' (tipo {t.type})")


def build_parser(**kwargs):
        r"""Construye y devuelve el parser PLY.

        - Se delega en `yacc.yacc` pasando el módulo actual para que PLY
            identifique las funciones `p_*` definidas aquí.
        - `kwargs` permite opciones como `debug` u `optimize`.
        """
        import sys
        return yacc.yacc(module=sys.modules[__name__], **kwargs)


# ------ Validación semántica de la estructura específica ------

date_time_re = re.compile(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$')
date_re = re.compile(r'^\d{2}/\d{2}/\d{4}$')
limite_re= re.compile(r'^\[(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\]$')
cedula_re = re.compile(r'^\d{8}$')

# Parametros validos para la seccion "Biometria Hematica"
PARAMETROS_VALIDOS = {
    'Leucocitos',
    'Eritrocitos',
    'Hemoglobina',
    'Hematocrito',
    'Plaquetas',
    'Neutrofilos',
    'Linfocitos',
    'Monocitos'
}


def validate_structure(data):
    r"""Validación semántica del esquema.

    Comprueba que el resultado del parseo contenga los campos
    obligatorios y que tengan el tipo/formato esperado. Esta
    validación es específica del ejercicio y no forma parte de la
    gramática.

    Devuelve `(True, None)` si la estructura es correcta, o
    `(False, mensaje_error)` con una explicación en caso contrario.
    """
    if not isinstance(data, dict):
        return False, 'La raíz no es un objeto JSON'

    required_top = ['folio', 'fecha_toma', 'fecha_validacion', 'paciente', 'seccion', 'parametros', 'firma']
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
    # Validar paciente
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
        return False, "'paciente.edad' debe ser un número entero positivo"
    # Validar seccion
    if not isinstance(data['seccion'], str):
        return False, "El campo 'seccion' debe ser una cadena"
    if data['seccion'] != 'Biometria Hematica':
        return False, f"La seccion debe ser 'Biometria Hematica', se encontro '{data['seccion']}'"

    # Validar parametros
    parametros = data['parametros']
    if not isinstance(parametros, list):
        return False, "El campo 'parametros' debe ser un array"
    if len(parametros) == 0:
        return False, "El campo 'parametros' no puede estar vacio"

    for i, param in enumerate(parametros):
        if not isinstance(param, dict):
            return False, f"El parametro {i+1} debe ser un objeto"

        required_param = ['nombre', 'resultado', 'unidad', 'limite']
        for k in required_param:
            if k not in param:
                return False, f"Falta campo '{k}' en parametro {i+1}"

        # Validar que el nombre sea un parametro valido
        if param['nombre'] not in PARAMETROS_VALIDOS:
            return False, f"'{param['nombre']}' no pertenece a la seccion 'Biometria Hematica'"

        # Validar resultado
        if not isinstance(param['resultado'], (int, float)):
            return False, f"El resultado del parametro '{param['nombre']}' debe ser numerico"

        # Validar unidad
        if not isinstance(param['unidad'], str):
            return False, f"La unidad del parametro '{param['nombre']}' debe ser una cadena"

        # Validar limite
        if not isinstance(param['limite'], str):
            return False, f"El limite del parametro '{param['nombre']}' debe ser una cadena"
        if not limite_re.match(param['limite']):
            return False, f"El limite '{param['limite']}' no cumple el formato '[x - y]'"

        # Validar nota si existe
        if 'nota' in param:
            if param['nota'] not in ('*', '**', '+'):
                return False, f"La nota del parametro '{param['nombre']}' debe ser '*', '**' o '+'"

    # Validar firma
    firma = data['firma']
    if not isinstance(firma, dict):
        return False, "El campo 'firma' debe ser un objeto"

    required_firma = ['responsable', 'cedula']
    for k in required_firma:
        if k not in firma:
            return False, f"Falta campo '{k}' en 'firma'"

    if not isinstance(firma['responsable'], str):
        return False, "'firma.responsable' debe ser una cadena"
    if not isinstance(firma['cedula'], str):
        return False, "'firma.cedula' debe ser una cadena"
    if not cedula_re.match(firma['cedula']):
        return False, "La cedula profesional debe tener exactamente 8 digitos"


    return True, None


def parse_text(text):
    r"""Función de alto nivel para parsear y validar texto JSON.

    - Construye el lexer y parser, ejecuta el análisis sintáctico
      y luego la validación semántica.
    - Retorna `(data, None)` si todo es correcto o `(None, mensaje)`
      cuando ocurre un error.
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
  },
  "medico_solicitante": "Dr. Rafael Barbera Vazquez",
  "seccion": "Biometria Hematica",
  "parametros": [
    {"nombre": "Leucocitos", "resultado": 5.9, "unidad": "10^3/uL", "limite": "[4.5 - 10.0]"},
    {"nombre": "Eritrocitos", "resultado": 4.82, "unidad": "10^6/uL", "limite": "[4.3 - 5.8]"},
    {"nombre": "Hemoglobina", "resultado": 14.2, "unidad": "g/dL", "limite": "[12.0 - 16.0]"},
    {"nombre": "Hematocrito", "resultado": 42.5, "unidad": "%", "limite": "[36.0 - 46.0]"},
    {"nombre": "Plaquetas", "resultado": 210, "unidad": "10^3/uL", "limite": "[150 - 400]", "nota": "+"}
  ],
  "firma": {
    "responsable": "Q.F.B. Alejandra Ruiz Salgado",
    "cedula": "09874563"
  }
}'''

    data, err = parse_text(text)
    if err:
        print('INVALID:', err)
    else:
        print('VALID: objeto parseado correctamente')
        import json
        print(json.dumps(data, ensure_ascii=False, indent=2))
