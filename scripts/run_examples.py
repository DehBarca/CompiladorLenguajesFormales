# Script de prueba para ejecutar ejemplos contra src/parser.py
# Ejecutar: .\env\Scripts\python .\scripts\run_examples.py

import sys, json
from pprint import pprint
sys.path.insert(0, 'src')
from parser import parse_text

EXAMPLES = [
    ("1 - Válido completo", '''{
  "folio": 15502427,
  "fecha_toma": "14/06/2020 07:51:57",
  "fecha_validacion": "14/06/2020 17:08:05",
  "paciente": {
    "nombre": "Ramírez Guzmán, María",
    "fecha_nacimiento": "25/04/1985",
    "sexo": "F",
    "edad": 35
  }
}'''),

    ("2 - Falta 'folio' (inválido)", '''{
  "fecha_toma": "14/06/2020 07:51:57",
  "fecha_validacion": "14/06/2020 17:08:05",
  "paciente": {
    "nombre": "María",
    "fecha_nacimiento": "25/04/1985",
    "sexo": "F",
    "edad": 35
  }
}'''),

    ("3 - Formato fecha inválido (fecha_toma)", '''{
  "folio": 123,
  "fecha_toma": "2020-06-14 07:51:57",
  "fecha_validacion": "14/06/2020 17:08:05",
  "paciente": {
    "nombre": "Test",
    "fecha_nacimiento": "25/04/1985",
    "sexo": "M",
    "edad": 40
  }
}'''),

    ("4 - Tipo incorrecto (folio como string)", '''{
  "folio": "15502427",
  "fecha_toma": "14/06/2020 07:51:57",
  "fecha_validacion": "14/06/2020 17:08:05",
  "paciente": {
    "nombre": "Ana",
    "fecha_nacimiento": "10/10/1990",
    "sexo": "F",
    "edad": 30
  }
}'''),

    ("5 - Objeto vacío (inválido)", '{}')
]

for title, text in EXAMPLES:
    print('\n' + '='*60)
    print(title)
    print('-' * 60)
    data, err = parse_text(text)
    if err:
        print('Result: INVALID')
        print('Reason:', err)
    else:
        print('Result: VALID')
        pprint(data, width=120)

print('\nPruebas finalizadas.')
