# Validador de JSON para Datos Médicos

Proyecto de **Lenguajes Formales** que implementa un analizador léxico y sintáctico para validar archivos JSON con una estructura específica de datos de pacientes médicos.

## 📋 Descripción

Este proyecto utiliza **PLY (Python Lex-Yacc)** para implementar:
- **Analizador léxico (`lexer.py`)**: Tokeniza el texto JSON en elementos básicos (llaves, comas, cadenas, números)
- **Analizador sintáctico (`parser.py`)**: Valida la estructura JSON y verifica que cumpla con el formato requerido

### Estructura JSON esperada (Reporte de Análisis de Sangre)

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
  },
  "medico_solicitante": "Dr. Rafael Barbera Vazquez",
  "seccion": "Biometria Hematica",
  "parametros": [
    {
      "nombre": "Leucocitos",
      "resultado": 5.9,
      "unidad": "10^3/uL",
      "limite": "[4.5 - 10.0]"
    },
    {
      "nombre": "Hemoglobina",
      "resultado": 14.2,
      "unidad": "g/dL",
      "limite": "[12.0 - 16.0]",
      "nota": "+"
    }
  ],
  "firma": {
    "responsable": "Q.F.B. Alejandra Ruiz Salgado",
    "cedula": "09874563"
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

**Opción 1: Usar requirements.txt (Recomendado)**
```powershell
pip install -r requirements.txt
```

**Opción 2: Instalación manual**

```powershell
# Instalar PLY (requerido para lexer/parser)
pip install ply

# Instalar pytest (requerido para tests)
pip install pytest
```

## 🚀 Uso

### Validar un archivo JSON

``` powershell
# Windows (PowerShell) - Usar ruta completa al entorno virtual
Get-Content .\tests\reporte_valido.json -Raw | .\env\Scripts\python .\src\parser.py
Get-Content .\tests\reporte_error_formato.json -Raw | .\env\Scripts\python .\src\parser.py
Get-Content .\tests\reporte_error_semantico.json -Raw | .\env\Scripts\python .\src\parser.py
Get-Content .\tests\reporte_error_sintactico.txt -Raw | .\env\Scripts\python .\src\parser.py
```

```bash
# Linux/Mac (Bash)
cat tests/reporte_valido.json | python src/parser.py
cat tests/reporte_error_formato.json | python src/parser.py
cat tests/reporte_error_semantico.json | python src/parser.py
cat tests/reporte_error_sintactico.txt | python src/parser.py
cat tests/reporte_error_valido.json | python src/parser.py
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

## ⚡ Comandos Rápidos

### Validación Rápida

```powershell
# Probar con archivos de ejemplo incluidos (PowerShell)
Get-Content .\tests\reporte_valido.json -Raw | .\env\Scripts\python .\src\parser.py
Get-Content .\tests\reporte_error_formato.json -Raw | .\env\Scripts\python .\src\parser.py
Get-Content .\tests\reporte_error_semantico.json -Raw | .\env\Scripts\python .\src\parser.py
Get-Content .\tests\reporte_error_sintactico.txt -Raw | .\env\Scripts\python .\src\parser.py

# Alternativa con variable (más legible para comandos largos)
$content = Get-Content .\tests\reporte_valido.json -Raw; $content | .\env\Scripts\python .\src\parser.py
```

### Ejecutar Script de Ejemplos

```powershell
# Ejecutar todos los ejemplos de una vez
.\env\Scripts\python .\scripts\run_examples.py

# Ejecutar ejemplos con más detalle
.\env\Scripts\python .\scripts\run_examples2.py
```

### Tests y Desarrollo

```powershell
# Ejecutar todos los tests (recomendado)
pytest tests\ -v

# Tests con cobertura
pytest tests\ --cov=src --cov-report=html

# Tests rápidos (sin verbose)
pytest tests\ -q

# Solo tests del lexer
pytest tests\test_lexer.py -v

# Solo tests del parser  
pytest tests\test_parser.py -v
```

### Limpieza y Mantenimiento

```powershell
# Limpiar archivos generados por PLY
Remove-Item src\parser.out, src\parsetab.py -ErrorAction SilentlyContinue

# Limpiar cache de Python
Get-ChildItem -Recurse -Name __pycache__ | Remove-Item -Recurse -Force

# Limpiar cache de pytest
Remove-Item .pytest_cache -Recurse -Force -ErrorAction SilentlyContinue

# Regenerar archivos PLY (tras cambios en gramática)
.\env\Scripts\python -c "import sys; sys.path.append('src'); from parser import parse_text; print('Parser regenerado')"
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

El proyecto incluye **36 tests automatizados** usando pytest que verifican:
- ✅ Tokenización correcta del lexer (13 tests)
- ✅ Validación sintáctica y semántica del parser (23 tests)
- ✅ Manejo de errores y casos límite
- ✅ Preservación de caracteres UTF-8 (acentos, ñ, etc.)

### Ejecutar todos los tests

```powershell
# Con entorno virtual activado
pytest tests/ -v

# Alternativa usando el Python del entorno virtual (Windows)
.\env\Scripts\python -m pytest tests/ -v
```

### Ejecutar tests específicos

```powershell
# Solo tests del lexer
pytest tests/test_lexer.py -v

# Solo tests del parser
pytest tests/test_parser.py -v

# Test específico
pytest tests/test_parser.py::TestParser::test_valid_complete_blood_analysis -v
```

### Cobertura de tests

```powershell
# Instalar pytest-cov
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest tests/ --cov=src --cov-report=html
```

**Resultado esperado (ejemplo):**
```
tests/test_lexer.py::TestLexer::test_empty_object PASSED            [  3%]
tests/test_lexer.py::TestLexer::test_simple_pair PASSED             [  7%]
...
tests/test_parser.py::TestParser::test_valid_complete_blood_analysis PASSED   [ 46%]
...
========================= 36 passed in 0.08s =========================
```

## 📁 Estructura del Proyecto

```
CompiladorLenguajesFormales/
│
├── src/                     # Código fuente principal
│   ├── lexer.py            # Analizador léxico (tokenización)
│   ├── parser.py           # Analizador sintáctico (validación)
│   ├── main.py             # Punto de entrada alternativo
│   ├── parser.out          # Tabla LALR generada por PLY
│   └── parsetab.py         # Cache del parser PLY
│
├── tests/                   # Tests y ejemplos de validación
│   ├── test_lexer.py       # 13 tests del analizador léxico
│   ├── test_parser.py      # 23 tests del analizador sintáctico
│   ├── reporte_valido.json # Ejemplo válido completo
│   ├── reporte_error_formato.json    # Error formato límites
│   ├── reporte_error_semantico.json  # Error parámetro inválido
│   └── reporte_error_sintactico.txt  # Error JSON incompleto
│
├── scripts/                 # Scripts de utilidad
│   ├── run_examples.py     # Ejecuta ejemplos básicos
│   └── run_examples2.py    # Ejecuta ejemplos extendidos
│
├── env/                     # Entorno virtual Python
├── .pytest_cache/           # Cache de pytest (generado)
├── __pycache__/             # Cache de Python (generado)
│
├── .git/                    # Control de versiones Git
├── .gitignore              # Archivos ignorados por Git
├── requirements.txt        # Dependencias Python
└── README.md               # Documentación (este archivo)
```

### Archivos Importantes

- **`src/parser.py`**: Archivo principal. Contiene la lógica de validación.
- **`tests/reporte_*.json`**: Casos de prueba reales para validar funcionalidad.
- **`requirements.txt`**: Lista exacta de dependencias con versiones.
- **`.gitignore`**: Excluye archivos generados (cache, entorno virtual).

## 🛠️ Troubleshooting / Solución de Problemas

### Errores Comunes

**Error: "No module named 'ply'"**
```powershell
# Solución: Instalar PLY
pip install ply
# o
pip install -r requirements.txt
```

**Error: "Generating LALR tables" (primera ejecución)**
- Es normal. PLY genera las tablas la primera vez.
- Los archivos `parser.out` y `parsetab.py` se crean automáticamente.

**Error: "Error de sintaxis: Error de sintaxis"**
- Verificar que el JSON esté bien formado (llaves, comas, etc.)
- Usar un validador JSON online para verificar sintaxis básica.

**Error: "Falta campo requerido en raíz"**
- Asegurarse de que el JSON incluya TODOS los campos:
  - `folio`, `fecha_toma`, `fecha_validacion`, `paciente`
  - `medico_solicitante`, `seccion`, `parametros`, `firma`

**Tests fallan con "ModuleNotFoundError"**
```powershell
# Ejecutar desde la raíz del proyecto
cd C:\ruta\al\proyecto\CompiladorLenguajesFormales
pytest tests\ -v
```

## 🔍 Notas Técnicas

1. **PLY genera archivos automáticamente**: `parser.out` y `parsetab.py` son creados por PLY la primera vez que ejecutas el parser
2. **Espacios en blanco ignorados**: El lexer ignora espacios, tabulaciones y saltos de línea
3. **Manejo de errores**: El parser captura errores de sintaxis y validación, mostrando mensajes descriptivos
4. **Formato de fechas**: Las fechas se validan solo por formato (regex), no por validez semántica
5. **UTF-8**: Los caracteres con acentos y ñ se preservan correctamente
6. **Tests**: 36 tests automatizados con 100% de éxito verifican el funcionamiento completo

## 👥 Autores

- Barraza C. Diego A.
- Romo M. Diego
- Portillo M. Pablo
- Caballero V. Renata I.
