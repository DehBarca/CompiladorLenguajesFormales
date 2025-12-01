r"""
Este módulo define las reglas léxicas (tokens) utilizadas por el parser
en `src/parser.py`. Está intencionado para tokenizar únicamente el
subconjunto de JSON que usamos en la práctica (objetos, cadenas y números
enteros). No implementa booleanos, null ni arrays completos.

Tokens soportados:
- `LBRACE` / `RBRACE`: llaves izquierda/derecha `{` `}`
- `COLON`: `:`
- `COMMA`: `,`
- `STRING`: cadena entre comillas dobles (soporta escapes básicos `\n`, `\t`, `\\", "\\`)
- `NUMBER`: números enteros (se convierten a `int`)

La función `build_lexer()` construye y devuelve el lexer de PLY para
ser usado por el parser. El módulo también incluye un pequeño modo de
prueba cuando se ejecuta como script.
"""

import re
import ply.lex as lex

# Lista de nombres de tokens usada por PLY
tokens = (
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'COLON',
    'COMMA',
    'STRING',
    'NUMBER',
)

# Reglas simples (expresiones regulares) para símbolos literales.
# Cada nombre `t_<n>` define el patrón para el token <n>.
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLON = r':'
t_COMMA = r','

# Ignorar espacios en blanco y saltos de línea.
# PLY automáticamente omite estos caracteres al tokenizar.
t_ignore = ' \t\r\n'

def t_STRING(t):
        r'"([^"\\]|\\.)*"'
        """Procesa literales de cadena JSON.
        """
        # Remueve las comillas alrededor del literal
        s = t.value[1:-1]
        # Reemplazos simples para manejar escapes comunes en JSON
        s = s.replace('\\n', '\n')
        s = s.replace('\\t', '\t')
        s = s.replace('\\r', '\r')
        s = s.replace('\\"', '"')
        s = s.replace('\\\\', '\\')
        t.value = s
        return t

def t_NUMBER(t):
    r'-?\d+(\.\d+)?'
    """Reconoce números enteros consecutivos y decimales.

    Convierte el valor de texto a `int` o 'float' segun corresponda para que el parser trabaje
    con tipos numéricos directamente.
    """
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_error(t):
    """Manejador de errores léxicos.

    Se ejecuta cuando no existe ningún token que coincida con el
    carácter actual. Muestra un mensaje y avanza un carácter para
    intentar continuar el análisis.
    """
    print(f"Caracter inválido en entrada: '{t.value[0]}' (en posición {t.lexpos})")
    t.lexer.skip(1)

def build_lexer(**kwargs):
    r"""Construye y devuelve el lexer PLY.

    - Devuelve un objeto lexer configurado con las reglas definidas en
      este módulo. Se pasa `module=sys.modules[__name__]` a `lex.lex`
      para que PLY encuentre las funciones `t_*` aquí definidas.
    - `kwargs` permite pasar opciones de PLY como `optimize=True`.

    Uso:
        lexer = build_lexer()
        lexer.input(text)
        for tok in lexer: print(tok)
    """
    import sys
    return lex.lex(module=sys.modules[__name__], **kwargs)

if __name__ == '__main__':
    # Prueba rápida del lexer leyendo entrada estándar
    import sys
    data = sys.stdin.read() or '{ "a": 1 }'
    l = build_lexer()
    l.input(data)
    for tok in l:
        print(tok)
