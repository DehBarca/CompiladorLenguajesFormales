# Validador de JSON para Datos Médicos

Proyecto de **Lenguajes Formales y Compiladores** que implementa un analizador léxico y sintáctico para validar archivos JSON con una estructura específica de datos de pacientes médicos.

## 📋 Descripción

Este proyecto utiliza **PLY (Python Lex-Yacc)** para implementar:
- **Analizador léxico (`lexer.py`)**: Tokeniza el texto JSON en elementos básicos (llaves, comas, cadenas, números)
- **Analizador sintáctico (`parser.py`)**: Valida la estructura JSON y verifica que cumpla con el formato requerido

### Estructura JSON esperada

```json
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
```

## 🛠️ Instalación

### 1. Crear entorno virtual

```powershell
# Windows (PowerShell)
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 2. Instalar dependencias

```powershell
# Instalar PLY (requerido)
pip install ply

# Instalar pytest (opcional, para ejecutar tests)
pip install pytest
```

O usando el archivo de requirements:

```powershell
pip install -r requirements.txt
```

## 🚀 Uso

### Validar un archivo JSON

```powershell
# Windows (PowerShell)
Get-Content .\examples\ejemplo.json -Raw | python .\src\parser.py

# Linux/Mac
cat examples/ejemplo.json | python src/parser.py
```

### Probar con el ejemplo incluido

```powershell
# Ejecutar sin argumentos usa el ejemplo por defecto
# Presiona Ctrl+Z (Windows) o Ctrl+D (Linux/Mac) para enviar EOF
python .\src\parser.py
```

### Salida esperada

**JSON válido:**
```
Generating LALR tables
VALID: objeto parseado correctamente
{
  "folio": 15502427,
  "fecha_toma": "14/06/2020 07:51:57",
  ...
}
```

**JSON inválido:**
```
INVALID: Error de validación: Falta campo requerido en raíz: 'folio'
```

## 📚 Componentes del Proyecto

### `lexer.py` - Analizador Léxico

Implementa las **reglas léxicas** (tokens) usando PLY:

| Token | Descripción | Ejemplo |
|-------|-------------|---------|
| `LBRACE` | Llave izquierda | `{` |
| `RBRACE` | Llave derecha | `}` |
| `COLON` | Dos puntos | `:` |
| `COMMA` | Coma | `,` |
| `STRING` | Cadena entre comillas | `"texto"` |
| `NUMBER` | Número entero | `123` |

**Función principal:**
- `build_lexer()`: Construye y devuelve el lexer

**Ejemplo de uso del lexer:**
```python
import sys
sys.path.insert(0, 'src')
from lexer import build_lexer

lexer = build_lexer()
lexer.input('{ "clave": 123 }')
for tok in lexer:
    print(tok)
```

### `parser.py` - Analizador Sintáctico

Implementa la **gramática libre de contexto (GLC)** y validación semántica:

#### Reglas sintácticas (gramática)

```
start   → object
object  → { } | { members }
members → pair | members , pair
pair    → STRING : value
value   → STRING | NUMBER | object
```

#### Validación semántica

Verifica que el JSON contenga:

**Campos raíz (obligatorios):**
- `folio`: número entero
- `fecha_toma`: cadena con formato `dd/mm/yyyy HH:MM:SS`
- `fecha_validacion`: cadena con formato `dd/mm/yyyy HH:MM:SS`
- `paciente`: objeto con subcampos

**Campos en `paciente` (obligatorios):**
- `nombre`: cadena
- `fecha_nacimiento`: cadena con formato `dd/mm/yyyy`
- `sexo`: cadena de un carácter (ej: `"M"`, `"F"`)
- `edad`: número entero

**Función principal:**
- `parse_text(text)`: Parsea y valida el texto JSON
  - Retorna `(data, None)` si es válido
  - Retorna `(None, mensaje_error)` si hay errores

**Ejemplo de uso del parser:**
```python
import sys
sys.path.insert(0, 'src')
from parser import parse_text

text = '{ "folio": 123, ... }'
data, error = parse_text(text)
if error:
    print(f"Error: {error}")
else:
    print(f"Válido: {data}")
```

## 🧪 Tests

El proyecto incluye **26 tests automatizados** usando pytest que verifican:
- ✅ Tokenización correcta del lexer (11 tests)
- ✅ Validación sintáctica del parser (15 tests)
- ✅ Manejo de errores y casos límite
- ✅ Preservación de caracteres UTF-8 (acentos, ñ, etc.)

### Ejecutar todos los tests

```powershell
# Con entorno virtual activado
pytest tests/ -v

# Sin activar entorno (Windows)
.\env\Scripts\python -m pytest tests/ -v
```

### Ejecutar tests específicos

```powershell
# Solo tests del lexer
pytest tests/test_lexer.py -v

# Solo tests del parser
pytest tests/test_parser.py -v

# Test específico
pytest tests/test_parser.py::TestParser::test_valid_complete_json -v
```

### Cobertura de tests

```powershell
# Instalar pytest-cov
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest tests/ --cov=src --cov-report=html
```

**Resultado esperado:**
```
tests/test_lexer.py::TestLexer::test_empty_object PASSED            [  3%]
tests/test_lexer.py::TestLexer::test_simple_pair PASSED             [  7%]
...
tests/test_parser.py::TestParser::test_valid_complete_json PASSED   [ 46%]
...
========================= 26 passed in 0.08s =========================
```

## 📁 Estructura del Proyecto

```
CompiladorLenguajesFormales/
│
├── src/                     # Código fuente
│   ├── lexer.py            # Analizador léxico
│   └── parser.py           # Analizador sintáctico
│
├── tests/                   # Tests unitarios
│   ├── test_lexer.py       # Tests del lexer
│   └── test_parser.py      # Tests del parser
│
├── examples/                # Archivos de ejemplo
│   └── ejemplo.json        # JSON válido de ejemplo
│
├── env/                     # Entorno virtual 
├── .pytest_cache/           # Cache de pytest 
├── __pycache__/             # Cache de Python 
├── parser.out               # Tabla LALR de PLY 
├── parsetab.py              # Cache del parser PLY 
│
├── .gitignore
├── requirements.txt
└── README.md                # Documentación
```

## 🔍 Notas Técnicas

1. **PLY genera archivos automáticamente**: `parser.out` y `parsetab.py` son creados por PLY la primera vez que ejecutas el parser
2. **Espacios en blanco ignorados**: El lexer ignora espacios, tabulaciones y saltos de línea
3. **Manejo de errores**: El parser captura errores de sintaxis y validación, mostrando mensajes descriptivos
4. **Formato de fechas**: Las fechas se validan solo por formato (regex), no por validez semántica
5. **UTF-8**: Los caracteres con acentos y ñ se preservan correctamente
6. **Tests**: 26 tests automatizados con 100% de éxito verifican el funcionamiento completo

## 👥 Autores

- Barraza C. Diego A.
- Romo M. Diego