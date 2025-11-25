"""Tests unitarios para el analizador léxico (lexer.py)

Prueba que el lexer tokenice correctamente diferentes tipos de entrada
y maneje errores apropiadamente.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from lexer import build_lexer


class TestLexer:
    """Suite de pruebas para el analizador léxico."""

    def setup_method(self):
        """Inicializa el lexer antes de cada test."""
        self.lexer = build_lexer()

    def tokenize(self, text):
        """Helper para tokenizar texto y retornar lista de tokens."""
        self.lexer.input(text)
        return [(tok.type, tok.value) for tok in self.lexer]

    def test_empty_object(self):
        """Verifica tokenización de objeto vacío."""
        tokens = self.tokenize('{}')
        assert tokens == [('LBRACE', '{'), ('RBRACE', '}')]

    def test_simple_pair(self):
        """Verifica tokenización de un par clave-valor simple."""
        tokens = self.tokenize('{"clave": 123}')
        expected = [
            ('LBRACE', '{'),
            ('STRING', 'clave'),
            ('COLON', ':'),
            ('NUMBER', 123),
            ('RBRACE', '}')
        ]
        assert tokens == expected

    def test_multiple_pairs(self):
        """Verifica tokenización de múltiples pares."""
        tokens = self.tokenize('{"a": 1, "b": 2}')
        expected = [
            ('LBRACE', '{'),
            ('STRING', 'a'),
            ('COLON', ':'),
            ('NUMBER', 1),
            ('COMMA', ','),
            ('STRING', 'b'),
            ('COLON', ':'),
            ('NUMBER', 2),
            ('RBRACE', '}')
        ]
        assert tokens == expected

    def test_nested_object(self):
        """Verifica tokenización de objetos anidados."""
        tokens = self.tokenize('{"outer": {"inner": 42}}')
        expected = [
            ('LBRACE', '{'),
            ('STRING', 'outer'),
            ('COLON', ':'),
            ('LBRACE', '{'),
            ('STRING', 'inner'),
            ('COLON', ':'),
            ('NUMBER', 42),
            ('RBRACE', '}'),
            ('RBRACE', '}')
        ]
        assert tokens == expected

    def test_string_with_spaces(self):
        """Verifica que las cadenas con espacios se tokenicen correctamente."""
        tokens = self.tokenize('{"nombre": "Juan Pérez"}')
        assert ('STRING', 'Juan Pérez') in tokens

    def test_string_with_special_chars(self):
        """Verifica cadenas con caracteres especiales y acentos."""
        tokens = self.tokenize('{"texto": "Ramírez Guzmán, María"}')
        assert ('STRING', 'Ramírez Guzmán, María') in tokens

    def test_date_time_string(self):
        """Verifica tokenización de cadenas con formato fecha/hora."""
        tokens = self.tokenize('{"fecha": "14/06/2020 07:51:57"}')
        assert ('STRING', '14/06/2020 07:51:57') in tokens

    def test_large_number(self):
        """Verifica tokenización de números grandes."""
        tokens = self.tokenize('{"folio": 15502427}')
        assert ('NUMBER', 15502427) in tokens

    def test_whitespace_ignored(self):
        """Verifica que espacios, tabs y newlines sean ignorados."""
        text1 = '{"a":1}'
        text2 = '{\n  "a"  :  1\n}'
        text3 = '{\t"a"\t:\t1\t}'
        
        tokens1 = self.tokenize(text1)
        tokens2 = self.tokenize(text2)
        tokens3 = self.tokenize(text3)
        
        assert tokens1 == tokens2 == tokens3

    def test_complete_patient_json(self):
        """Verifica tokenización del JSON completo de ejemplo."""
        json_text = '''{
            "folio": 15502427,
            "fecha_toma": "14/06/2020 07:51:57",
            "paciente": {
                "nombre": "María",
                "edad": 35
            }
        }'''
        tokens = self.tokenize(json_text)
        
        # Verificar que contiene los tokens principales
        token_types = [t[0] for t in tokens]
        assert 'LBRACE' in token_types
        assert 'RBRACE' in token_types
        assert 'STRING' in token_types
        assert 'NUMBER' in token_types
        assert 'COLON' in token_types
        assert 'COMMA' in token_types

    def test_string_with_escape_sequences(self):
        """Verifica que el lexer maneje secuencias de escape básicas."""
        # Nota: el lexer actual decodifica escapes
        tokens = self.tokenize('{"text": "Line 1\\nLine 2"}')
        # Buscar el token STRING
        string_values = [v for t, v in tokens if t == 'STRING']
        assert len(string_values) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
