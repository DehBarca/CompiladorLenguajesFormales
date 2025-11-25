"""Tests unitarios para el analizador sintáctico (parser.py)

Prueba que el parser valide correctamente la estructura JSON esperada
y detecte diferentes tipos de errores.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from parser import parse_text


class TestParser:
    """Suite de pruebas para el analizador sintáctico."""

    def test_valid_complete_json(self):
        """Verifica que un JSON válido completo sea aceptado."""
        json_text = '''{
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
        data, error = parse_text(json_text)
        assert error is None
        assert data is not None
        assert data['folio'] == 15502427
        assert data['paciente']['nombre'] == "Ramírez Guzmán, María"

    def test_missing_folio(self):
        """Verifica que falle si falta el campo 'folio'."""
        json_text = '''{
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {
                "nombre": "María",
                "fecha_nacimiento": "25/04/1985",
                "sexo": "F",
                "edad": 35
            }
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert error is not None
        assert "folio" in error.lower()

    def test_missing_fecha_toma(self):
        """Verifica que falle si falta 'fecha_toma'."""
        json_text = '''{
            "folio": 123,
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {
                "nombre": "María",
                "fecha_nacimiento": "25/04/1985",
                "sexo": "F",
                "edad": 35
            }
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "fecha_toma" in error.lower()

    def test_missing_paciente(self):
        """Verifica que falle si falta el objeto 'paciente'."""
        json_text = '''{
            "folio": 123,
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05"
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "paciente" in error.lower()

    def test_missing_paciente_nombre(self):
        """Verifica que falle si falta 'paciente.nombre'."""
        json_text = '''{
            "folio": 123,
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {
                "fecha_nacimiento": "25/04/1985",
                "sexo": "F",
                "edad": 35
            }
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "nombre" in error.lower()

    def test_invalid_folio_type(self):
        """Verifica que falle si 'folio' no es un número."""
        json_text = '''{
            "folio": "not a number",
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {
                "nombre": "María",
                "fecha_nacimiento": "25/04/1985",
                "sexo": "F",
                "edad": 35
            }
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "folio" in error.lower()

    def test_invalid_fecha_toma_format(self):
        """Verifica que falle si 'fecha_toma' tiene formato incorrecto."""
        json_text = '''{
            "folio": 123,
            "fecha_toma": "2020-06-14 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {
                "nombre": "María",
                "fecha_nacimiento": "25/04/1985",
                "sexo": "F",
                "edad": 35
            }
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "fecha_toma" in error.lower()

    def test_invalid_fecha_nacimiento_format(self):
        """Verifica que falle si 'fecha_nacimiento' tiene formato incorrecto."""
        json_text = '''{
            "folio": 123,
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {
                "nombre": "María",
                "fecha_nacimiento": "1985-04-25",
                "sexo": "F",
                "edad": 35
            }
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "fecha_nacimiento" in error.lower()

    def test_invalid_edad_type(self):
        """Verifica que falle si 'edad' no es un número."""
        json_text = '''{
            "folio": 123,
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {
                "nombre": "María",
                "fecha_nacimiento": "25/04/1985",
                "sexo": "F",
                "edad": "35"
            }
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "edad" in error.lower()

    def test_syntax_error_missing_brace(self):
        """Verifica que detecte errores de sintaxis (llave faltante)."""
        json_text = '''{
            "folio": 123,
            "fecha_toma": "14/06/2020 07:51:57"
        '''  # Falta llave de cierre
        data, error = parse_text(json_text)
        assert data is None
        assert error is not None

    def test_syntax_error_missing_colon(self):
        """Verifica que detecte errores de sintaxis (dos puntos faltantes)."""
        json_text = '{"clave" 123}'
        data, error = parse_text(json_text)
        assert data is None
        assert error is not None

    def test_syntax_error_missing_comma(self):
        """Verifica que detecte errores de sintaxis (coma faltante)."""
        json_text = '{"a": 1 "b": 2}'
        data, error = parse_text(json_text)
        assert data is None
        assert error is not None

    def test_empty_object_invalid(self):
        """Verifica que un objeto vacío sea rechazado por falta de campos."""
        json_text = '{}'
        data, error = parse_text(json_text)
        assert data is None
        assert error is not None

    def test_valid_with_male_patient(self):
        """Verifica JSON válido con paciente masculino."""
        json_text = '''{
            "folio": 999,
            "fecha_toma": "01/01/2020 10:00:00",
            "fecha_validacion": "01/01/2020 15:00:00",
            "paciente": {
                "nombre": "García López, Juan",
                "fecha_nacimiento": "15/03/1990",
                "sexo": "M",
                "edad": 30
            }
        }'''
        data, error = parse_text(json_text)
        assert error is None
        assert data is not None
        assert data['paciente']['sexo'] == "M"

    def test_valid_with_different_numbers(self):
        """Verifica que acepte diferentes valores numéricos válidos."""
        json_text = '''{
            "folio": 1,
            "fecha_toma": "01/01/2020 00:00:00",
            "fecha_validacion": "01/01/2020 00:00:01",
            "paciente": {
                "nombre": "Test",
                "fecha_nacimiento": "01/01/2000",
                "sexo": "X",
                "edad": 20
            }
        }'''
        data, error = parse_text(json_text)
        assert error is None
        assert data['folio'] == 1
        assert data['paciente']['edad'] == 20


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
