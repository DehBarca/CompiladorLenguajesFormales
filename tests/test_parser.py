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

    def test_valid_complete_blood_analysis(self):
        """Verifica que un JSON de análisis de sangre válido completo sea aceptado."""
        json_text = '''{
            "folio": 15502427,
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {
                "nombre": "Ramírez Guzmán, María",
                "fecha_nacimiento": "25/04/1985",
                "sexo": "F",
                "edad": 35
            },
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [
                {"nombre": "Leucocitos", "resultado": 5.9, "unidad": "10^3/uL", "limite": "[4.5 - 10.0]"},
                {"nombre": "Hemoglobina", "resultado": 14.2, "unidad": "g/dL", "limite": "[12.0 - 16.0]"}
            ],
            "firma": {
                "responsable": "Q.F.B. Alejandra Ruiz Salgado",
                "cedula": "09874563"
            }
        }'''
        data, error = parse_text(json_text)
        assert error is None
        assert data is not None
        assert data['folio'] == 15502427
        assert data['paciente']['nombre'] == "Ramírez Guzmán, María"
        assert data['seccion'] == "Biometria Hematica"
        assert len(data['parametros']) == 2
        assert data['parametros'][0]['nombre'] == "Leucocitos"
        assert data['parametros'][0]['resultado'] == 5.9
        assert data['firma']['cedula'] == "09874563"

    def test_missing_required_fields(self):
        """Verifica que falle si faltan campos requeridos."""
        # Falta folio
        json_text = '''{
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {"nombre": "Test", "fecha_nacimiento": "25/04/1985", "sexo": "F", "edad": 35},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [{"nombre": "Leucocitos", "resultado": 5.9, "unidad": "10^3/uL", "limite": "[4.5 - 10.0]"}],
            "firma": {"responsable": "Dr. Test", "cedula": "12345678"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "folio" in error.lower()

    def test_missing_seccion(self):
        """Verifica que falle si falta 'seccion'."""
        json_text = '''{
            "folio": 123,
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {"nombre": "Test", "fecha_nacimiento": "25/04/1985", "sexo": "F", "edad": 35},
            "medico_solicitante": "Dr. Test",
            "parametros": [{"nombre": "Leucocitos", "resultado": 5.9, "unidad": "10^3/uL", "limite": "[4.5 - 10.0]"}],
            "firma": {"responsable": "Dr. Test", "cedula": "12345678"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "seccion" in error.lower()

    def test_missing_parametros(self):
        """Verifica que falle si falta el array 'parametros'."""
        json_text = '''{
            "folio": 123,
            "fecha_toma": "14/06/2020 07:51:57",
            "fecha_validacion": "14/06/2020 17:08:05",
            "paciente": {"nombre": "Test", "fecha_nacimiento": "25/04/1985", "sexo": "F", "edad": 35},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "firma": {"responsable": "Dr. Test", "cedula": "12345678"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "parametros" in error.lower()

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
            },
            "medico_solicitante": "Dr. Test",
            "seccion": "HEMATOLOGÍA",
            "parametros": [
                {
                    "nombre": "Glucosa en plasma",
                    "resultado": 85.5,
                    "limite": "[70 - 105]",
                    "unidad": "mg/dl"
                }
            ],
            "firma": {
                "responsable": "Dr. García",
                "cedula": "12345678"
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
            },
            "medico_solicitante": "Dr. Test",
            "seccion": "HEMATOLOGÍA",
            "parametros": [
                {
                    "nombre": "Glucosa en plasma",
                    "resultado": 85.5,
                    "limite": "[70 - 105]",
                    "unidad": "mg/dl"
                }
            ],
            "firma": {
                "responsable": "Dr. García",
                "cedula": "12345678"
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
            },
            "medico_solicitante": "Dr. Test",
            "seccion": "HEMATOLOGÍA",
            "parametros": [
                {
                    "nombre": "Glucosa en plasma",
                    "resultado": 85.5,
                    "limite": "[70 - 105]",
                    "unidad": "mg/dl"
                }
            ],
            "firma": {
                "responsable": "Dr. García",
                "cedula": "12345678"
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
            },
            "medico_solicitante": "Dr. Test",
            "seccion": "HEMATOLOGÍA",
            "parametros": [
                {
                    "nombre": "Glucosa en plasma",
                    "resultado": 85.5,
                    "limite": "[70 - 105]",
                    "unidad": "mg/dl"
                }
            ],
            "firma": {
                "responsable": "Dr. García",
                "cedula": "12345678"
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
            },
            "medico_solicitante": "Dr. Test",
            "seccion": "HEMATOLOGÍA",
            "parametros": [
                {
                    "nombre": "Glucosa en plasma",
                    "resultado": 85.5,
                    "limite": "[70 - 105]",
                    "unidad": "mg/dl"
                }
            ],
            "firma": {
                "responsable": "Dr. García",
                "cedula": "12345678"
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
            },
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometría Hemática",
            "parametros": [
                {
                    "nombre": "Hemoglobina",
                    "resultado": 14.2,
                    "limite": "[12.0 - 16.0]",
                    "unidad": "g/dl"
                }
            ],
            "firma": {
                "responsable": "Dr. García",
                "cedula": "12345678"
            }
        }'''
        data, error = parse_text(json_text)
        assert error is None
        assert data is not None
        assert data['paciente']['sexo'] == "M"

    def test_invalid_parameter_name(self):
        """Verifica que falle con nombre de parámetro inválido."""
        json_text = '''{
            "folio": 100,
            "fecha_toma": "01/01/2021 08:00:00",
            "fecha_validacion": "01/01/2021 10:00:00",
            "paciente": {"nombre": "Test", "fecha_nacimiento": "01/01/1990", "sexo": "M", "edad": 30},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [{"nombre": "Glucosa", "resultado": 90, "unidad": "mg/dL", "limite": "[70 - 100]"}],
            "firma": {"responsable": "Dr. X", "cedula": "12345678"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "Glucosa" in error and "no pertenece" in error

    def test_invalid_limite_format(self):
        """Verifica que falle con formato de límite incorrecto."""
        json_text = '''{
            "folio": 101,
            "fecha_toma": "02/02/2022 09:10:10",
            "fecha_validacion": "02/02/2022 12:00:00",
            "paciente": {"nombre": "Test2", "fecha_nacimiento": "02/02/1980", "sexo": "F", "edad": 45},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [{"nombre": "Leucocitos", "resultado": 6.1, "unidad": "10^3/uL", "limite": "4.5-10.0"}],
            "firma": {"responsable": "Dr. Y", "cedula": "87654321"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "formato" in error and "limite" in error

    def test_missing_cedula_in_firma(self):
        """Verifica que falle si falta cédula en firma."""
        json_text = '''{
            "folio": 102,
            "fecha_toma": "03/03/2023 07:00:00",
            "fecha_validacion": "03/03/2023 08:00:00",
            "paciente": {"nombre": "Test3", "fecha_nacimiento": "03/03/1975", "sexo": "M", "edad": 50},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [{"nombre": "Plaquetas", "resultado": 200, "unidad": "10^3/uL", "limite": "[150 - 400]"}],
            "firma": {"responsable": "Dr. Z"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "cedula" in error.lower()

    def test_non_numeric_resultado(self):
        """Verifica que falle con resultado no numérico."""
        json_text = '''{
            "folio": 103,
            "fecha_toma": "04/04/2024 06:30:00",
            "fecha_validacion": "04/04/2024 09:00:00",
            "paciente": {"nombre": "Test4", "fecha_nacimiento": "04/04/2000", "sexo": "F", "edad": 25},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [{"nombre": "Hemoglobina", "resultado": "catorce", "unidad": "g/dL", "limite": "[12.0 - 16.0]"}],
            "firma": {"responsable": "Dr. A", "cedula": "11223344"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "numerico" in error

    def test_empty_parametros_array(self):
        """Verifica que falle si el array de parámetros está vacío."""
        json_text = '''{
            "folio": 104,
            "fecha_toma": "05/05/2024 08:00:00",
            "fecha_validacion": "05/05/2024 10:00:00",
            "paciente": {"nombre": "Test5", "fecha_nacimiento": "05/05/1995", "sexo": "M", "edad": 29},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [],
            "firma": {"responsable": "Dr. B", "cedula": "22334455"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "vacio" in error

    def test_valid_seccion_with_accents(self):
        """Verifica que acepte sección con acentos."""
        json_text = '''{
            "folio": 105,
            "fecha_toma": "06/06/2024 09:00:00",
            "fecha_validacion": "06/06/2024 11:00:00",
            "paciente": {"nombre": "Test6", "fecha_nacimiento": "06/06/1990", "sexo": "F", "edad": 34},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [{"nombre": "Eritrocitos", "resultado": 4.5, "unidad": "10^6/uL", "limite": "[4.3 - 5.8]"}],
            "firma": {"responsable": "Dr. C", "cedula": "33445566"}
        }'''
        data, error = parse_text(json_text)
        assert error is None
        assert data['seccion'] == "Biometria Hematica"

    def test_invalid_cedula_format(self):
        """Verifica que falle si la cédula no tiene 8 dígitos."""
        json_text = '''{
            "folio": 106,
            "fecha_toma": "07/07/2024 10:00:00",
            "fecha_validacion": "07/07/2024 12:00:00",
            "paciente": {"nombre": "Test7", "fecha_nacimiento": "07/07/1985", "sexo": "M", "edad": 39},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [{"nombre": "Leucocitos", "resultado": 7.0, "unidad": "10^3/uL", "limite": "[4.5 - 10.0]"}],
            "firma": {"responsable": "Dr. D", "cedula": "123"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "cedula" in error and "8 digitos" in error

    def test_valid_with_optional_nota(self):
        """Verifica que acepte parámetros con nota opcional."""
        json_text = '''{
            "folio": 107,
            "fecha_toma": "08/08/2024 11:00:00",
            "fecha_validacion": "08/08/2024 13:00:00",
            "paciente": {"nombre": "Test8", "fecha_nacimiento": "08/08/1992", "sexo": "F", "edad": 32},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [
                {"nombre": "Plaquetas", "resultado": 350, "unidad": "10^3/uL", "limite": "[150 - 400]", "nota": "*"},
                {"nombre": "Leucocitos", "resultado": 8.5, "unidad": "10^3/uL", "limite": "[4.5 - 10.0]", "nota": "+"}
            ],
            "firma": {"responsable": "Dr. E", "cedula": "44556677"}
        }'''
        data, error = parse_text(json_text)
        assert error is None
        assert data['parametros'][0]['nota'] == "*"
        assert data['parametros'][1]['nota'] == "+"

    def test_invalid_nota_value(self):
        """Verifica que falle con valor de nota inválido."""
        json_text = '''{
            "folio": 108,
            "fecha_toma": "09/09/2024 12:00:00",
            "fecha_validacion": "09/09/2024 14:00:00",
            "paciente": {"nombre": "Test9", "fecha_nacimiento": "09/09/1988", "sexo": "M", "edad": 36},
            "medico_solicitante": "Dr. Test",
            "seccion": "Biometria Hematica",
            "parametros": [{"nombre": "Hemoglobina", "resultado": 15.0, "unidad": "g/dL", "limite": "[12.0 - 16.0]", "nota": "X"}],
            "firma": {"responsable": "Dr. F", "cedula": "55667788"}
        }'''
        data, error = parse_text(json_text)
        assert data is None
        assert "nota" in error


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
