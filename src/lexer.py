r"""
Analizador léxico (lexer) para una versión reducida de JSON usando PLY.

Reglas léxicas en este archivo:
- Llaves: `{` y `}` (tokens LBRACE y RBRACE)
- Dos puntos: `:` (token COLON)
- Coma: `,` (token COMMA)
- Cadenas: secuencias entre comillas dobles `"..."` (token STRING)
- Números enteros: secuencias de dígitos (token NUMBER)

La función `build_lexer()` construye y devuelve el lexer (objeto PLY).

El token `STRING` devuelve el contenido sin las comillas ni las secuencias de escape
convertidas (se usa `unicode_escape` para interpretar escapes como \n, \uXXXX, etc.).

Diseñado para ser simple y centrado en validar la estructura JSON del enunciado.
"""

import re
import ply.lex as lex

# Lista de nombres de tokens usada por PLY
tokens = (
    'LBRACE',
    'RBRACE',
    'COLON',
    'COMMA',
    'STRING',
    'NUMBER',
)

# Reglas simples para llaves, dos puntos y coma
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'
t_COMMA = r','

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t\r\n'

def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    # Remueve las comillas y maneja escapes básicos
    s = t.value[1:-1]
    # Procesar solo escapes comunes de JSON sin afectar UTF-8
    s = s.replace('\\n', '\n')
    s = s.replace('\\t', '\t')
    s = s.replace('\\r', '\r')
    s = s.replace('\\"', '"')
    s = s.replace('\\\\', '\\')
    t.value = s
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    # Al encontrar un carácter inválido, informar el error y avanzar
    print(f"Caracter inválido en entrada: '{t.value[0]}' (en posición {t.lexpos})")
    t.lexer.skip(1)

def build_lexer(**kwargs):
    r"""Construye y devuelve el lexer PLY.

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
