# Ejecuta 5 ejemplos que cumplen/no cumplen el esquema extendido del parser
# Uso: .\env\Scripts\python .\scripts\run_examples2.py

import sys
from pprint import pprint
sys.path.insert(0, 'src')
from parser import parse_text

examples = [
    ("1 - Válido completo", '''{
  "folio": 15502427,
  "fecha_toma": "14/06/2020 07:51:57",
  "fecha_validacion": "14/06/2020 17:08:05",
  "paciente": {
    "nombre": "Ramírez Guzmán, María",
    "fecha_nacimiento": "25/04/1985",
    "sexo": "F",
    "edad": 35
  },
  "seccion": "Biometria Hematica",
  "parametros": [
    {"nombre": "Leucocitos", "resultado": 5.9, "unidad": "10^3/uL", "limite": "[4.5 - 10.0]"},
    {"nombre": "Eritrocitos", "resultado": 4.82, "unidad": "10^6/uL", "limite": "[4.3 - 5.8]"},
    {"nombre": "Hemoglobina", "resultado": 14.2, "unidad": "g/dL", "limite": "[12.0 - 16.0]"}
  ],
  "firma": {"responsable": "Q.F.B. Alejandra Ruiz Salgado", "cedula": "09874563"}
}'''),

    ("2 - Nombre de parámetro inválido", '''{
  "folio": 100,
  "fecha_toma": "01/01/2021 08:00:00",
  "fecha_validacion": "01/01/2021 10:00:00",
  "paciente": {"nombre": "Test", "fecha_nacimiento": "01/01/1990", "sexo": "M", "edad": 30},
  "seccion": "Biometria Hematica",
  "parametros": [
    {"nombre": "Glucosa", "resultado": 90, "unidad": "mg/dL", "limite": "[70 - 100]"}
  ],
  "firma": {"responsable": "Dr. X", "cedula": "12345678"}
}'''),

    ("3 - Limite con formato incorrecto", '''{
  "folio": 101,
  "fecha_toma": "02/02/2022 09:10:10",
  "fecha_validacion": "02/02/2022 12:00:00",
  "paciente": {"nombre": "Test2", "fecha_nacimiento": "02/02/1980", "sexo": "F", "edad": 45},
  "seccion": "Biometria Hematica",
  "parametros": [
    {"nombre": "Leucocitos", "resultado": 6.1, "unidad": "10^3/uL", "limite": "4.5-10.0"}
  ],
  "firma": {"responsable": "Dr. Y", "cedula": "87654321"}
}'''),

    ("4 - Falta campo en firma (cedula)", '''{
  "folio": 102,
  "fecha_toma": "03/03/2023 07:00:00",
  "fecha_validacion": "03/03/2023 08:00:00",
  "paciente": {"nombre": "Test3", "fecha_nacimiento": "03/03/1975", "sexo": "M", "edad": 50},
  "seccion": "Biometria Hematica",
  "parametros": [
    {"nombre": "Plaquetas", "resultado": 200, "unidad": "10^3/uL", "limite": "[150 - 400]"}
  ],
  "firma": {"responsable": "Dr. Z"}
}'''),

    ("5 - Resultado no numérico", '''{
  "folio": 103,
  "fecha_toma": "04/04/2024 06:30:00",
  "fecha_validacion": "04/04/2024 09:00:00",
  "paciente": {"nombre": "Test4", "fecha_nacimiento": "04/04/2000", "sexo": "F", "edad": 25},
  "seccion": "Biometria Hematica",
  "parametros": [
    {"nombre": "Hemoglobina", "resultado": "catorce", "unidad": "g/dL", "limite": "[12.0 - 16.0]"}
  ],
  "firma": {"responsable": "Dr. A", "cedula": "11223344"}
}''')
]

for title, text in examples:
    print('\n' + '='*60)
    print(title)
    print('-'*60)
    data, err = parse_text(text)
    if err:
        print('INVALID')
        print('Reason:', err)
    else:
        print('VALID')
        pprint(data, width=120)

print('\nHecho.')
