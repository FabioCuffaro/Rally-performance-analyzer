This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where security check has been disabled.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Security check has been disabled - content may contain sensitive information
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.env.example
.gitignore
.streamlit/config.toml
.streamlit/secrets.example.toml
backend/__init__.py
backend/app/__init__.py
backend/app/config.py
backend/app/main.py
backend/app/models/__init__.py
backend/app/models/schemas.py
backend/app/routers/__init__.py
backend/app/routers/drivers.py
backend/app/routers/rally.py
backend/app/routers/stages.py
backend/app/services/__init__.py
backend/app/services/analytics.py
backend/app/services/data_loader.py
backend/tests/__init__.py
backend/tests/test_api.py
backend/tests/test_health.py
backend/tests/test_ingestion.py
conftest.py
dashboard/app.py
dashboard/components/api_client.py
dashboard/components/charts.py
dashboard/pages/01_stages.py
dashboard/pages/02_evolution.py
dashboard/pages/03_compare.py
data/processed/.gitkeep
data/processed/events.csv
data/processed/rallye_automobile_monte_carlo_entries.csv
data/processed/rallye_automobile_monte_carlo_overall.csv
data/processed/rallye_automobile_monte_carlo_stage_times.csv
data/processed/rallye_automobile_monte_carlo_stages.csv
data/raw/.gitkeep
docs/bloque-00-setup.md
docs/bloque-01-ingesta.md
docs/bloque-02-backend.md
docs/bloque-03-dashboard.md
docs/bloque-04-graficos.md
docs/bloque-05-deploy.md
docs/comandos.md
ingestion/__init__.py
ingestion/mock_data.py
ingestion/pipeline.py
ingestion/transformers.py
ingestion/wrc_client.py
Makefile
pytest.ini
README.md
render.yaml
requirements.txt
```

# Files

## File: .streamlit/config.toml
````toml
[theme]
base = "dark"
primaryColor = "#C8102E"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1A1A2E"
textColor = "#FFFFFF"

[server]
headless = true
enableCORS = false
port = 8501
````

## File: .streamlit/secrets.example.toml
````toml
# Copia este archivo como .streamlit/secrets.toml para produccion
# NO subir secrets.toml al repo (ya esta en .gitignore)

# URL de la API en produccion (Render)
# Cambia esta URL por la URL real de tu servicio en Render
DASHBOARD_API_URL = "https://rally-performance-analyzer-api.onrender.com"
````

## File: data/processed/events.csv
````
event_id,name,status,country,country_iso,date_start,date_finish
1,Rallye Automobile Monte Carlo,Completed,France,FR,2024-01-25T00:00:00,2024-01-28T00:00:00
2,Rally Sweden,Completed,Sweden,SE,2024-02-15T00:00:00,2024-02-18T00:00:00
3,Safari Rally Kenya,Completed,Kenya,KE,2024-03-28T00:00:00,2024-03-31T00:00:00
````

## File: data/processed/rallye_automobile_monte_carlo_entries.csv
````
entry_id,driver_name,driver_code,driver_nationality,codriver_name,manufacturer,car_number,group
201,Sébastien Ogier,OGI,FR,Vincent Landais,Toyota,17,WRC
202,Elfyn Evans,EVA,GB,Scott Martin,Toyota,33,WRC
203,Thierry Neuville,NEU,BE,Martijn Wydaeghe,Hyundai,11,WRC
204,Ott Tänak,TAN,EE,Martin Järveoja,Hyundai,6,WRC
205,Kalle Rovanperä,ROV,FI,Jonne Halttunen,Toyota,69,WRC
206,Ott Tänak,TAN,EE,Andreas Mikkelsen,Hyundai,8,WRC
````

## File: data/processed/rallye_automobile_monte_carlo_overall.csv
````
event_id,stage_id,entry_id,position,total_time_ms,total_time_s,total_time_str,diff_first_ms,diff_first_s,status,stage_code
1,101,201,1,834500,834.5,00:13:54.500,0,0.0,0,SS1
1,101,202,2,836200,836.2,00:13:56.200,1700,1.7,0,SS1
1,101,203,3,837800,837.8,00:13:57.800,3300,3.3,0,SS1
1,101,205,4,839100,839.1,00:13:59.100,4600,4.6,0,SS1
1,101,204,5,841000,841.0,00:14:01.000,6500,6.5,0,SS1
1,101,206,6,844300,844.3,00:14:04.300,9800,9.8,0,SS1
1,102,201,1,1408000,1408.0,00:23:28.000,0,0.0,0,SS2
1,102,203,2,1409800,1409.8,00:23:29.800,1800,1.8,0,SS2
1,102,202,3,1413600,1413.6,00:23:33.600,5600,5.6,0,SS2
1,102,205,4,1414300,1414.3,00:23:34.300,6300,6.3,0,SS2
1,102,204,5,1420800,1420.8,00:23:40.800,12800,12.8,0,SS2
1,102,206,6,1427400,1427.4,00:23:47.400,19400,19.4,0,SS2
1,103,201,1,2426000,2426.0,00:40:26.000,0,0.0,0,SS3
1,103,203,2,2430300,2430.3,00:40:30.300,4300,4.3,0,SS3
1,103,202,3,2435700,2435.7,00:40:35.700,9700,9.7,0,SS3
1,103,205,4,2439600,2439.6,00:40:39.600,13600,13.6,0,SS3
1,103,204,5,2449500,2449.5,00:40:49.500,23500,23.5,0,SS3
1,103,206,6,2461600,2461.6,00:41:01.600,35600,35.6,0,SS3
1,104,201,1,3158800,3158.8,00:52:38.800,0,0.0,0,SS4
1,104,203,2,3166300,3166.3,00:52:46.300,7500,7.5,0,SS4
1,104,202,3,3166900,3166.9,00:52:46.900,8100,8.1,0,SS4
1,104,205,4,3174100,3174.1,00:52:54.100,15300,15.3,0,SS4
1,104,204,5,3188900,3188.9,00:53:08.900,30100,30.1,0,SS4
1,104,206,6,3204700,3204.7,00:53:24.700,45900,45.9,0,SS4
1,105,201,1,3988500,3988.5,01:06:28.500,0,0.0,0,SS5
1,105,203,2,3997500,3997.5,01:06:37.500,9000,9.0,0,SS5
1,105,202,3,4000700,4000.7,01:06:40.700,12200,12.2,0,SS5
1,105,205,4,4002400,4002.4,01:06:42.400,13900,13.9,0,SS5
1,105,204,5,4025400,4025.4,01:07:05.400,36900,36.9,0,SS5
1,105,206,6,4045700,4045.7,01:07:25.700,57200,57.2,0,SS5
````

## File: data/processed/rallye_automobile_monte_carlo_stage_times.csv
````
event_id,stage_id,entry_id,position,time_ms,time_s,time_str,diff_first_ms,diff_first_s,diff_prev_ms,diff_prev_s,status,stage_code
1,101,201,1,834500,834.5,00:13:54.500,0,0.0,0,0.0,Completed,SS1
1,101,202,2,836200,836.2,00:13:56.200,1700,1.7,1700,1.7,Completed,SS1
1,101,203,3,837800,837.8,00:13:57.800,3300,3.3,1600,1.6,Completed,SS1
1,101,205,4,839100,839.1,00:13:59.100,4600,4.6,1300,1.3,Completed,SS1
1,101,204,5,841000,841.0,00:14:01.000,6500,6.5,1900,1.9,Completed,SS1
1,101,206,6,844300,844.3,00:14:04.300,9800,9.8,3300,3.3,Completed,SS1
1,102,203,1,572000,572.0,00:09:32.000,0,0.0,0,0.0,Completed,SS2
1,102,201,2,573500,573.5,00:09:33.500,1500,1.5,1500,1.5,Completed,SS2
1,102,205,3,575200,575.2,00:09:35.200,3200,3.2,1700,1.7,Completed,SS2
1,102,202,4,577400,577.4,00:09:37.400,5400,5.4,2200,2.2,Completed,SS2
1,102,204,5,579800,579.8,00:09:39.800,7800,7.8,2400,2.4,Completed,SS2
1,102,206,6,583100,583.1,00:09:43.100,11100,11.1,3300,3.3,Completed,SS2
1,103,201,1,1018000,1018.0,00:16:58.000,0,0.0,0,0.0,Completed,SS3
1,103,203,2,1020500,1020.5,00:17:00.500,2500,2.5,2500,2.5,Completed,SS3
1,103,202,3,1022100,1022.1,00:17:02.100,4100,4.1,1600,1.6,Completed,SS3
1,103,205,4,1025300,1025.3,00:17:05.300,7300,7.3,3200,3.2,Completed,SS3
1,103,204,5,1028700,1028.7,00:17:08.700,10700,10.7,3400,3.4,Completed,SS3
1,103,206,6,1034200,1034.2,00:17:14.200,16200,16.2,5500,5.5,Completed,SS3
1,104,202,1,731200,731.2,00:12:11.200,0,0.0,0,0.0,Completed,SS4
1,104,201,2,732800,732.8,00:12:12.800,1600,1.6,1600,1.6,Completed,SS4
1,104,205,3,734500,734.5,00:12:14.500,3300,3.3,1700,1.7,Completed,SS4
1,104,203,4,736000,736.0,00:12:16.000,4800,4.8,1500,1.5,Completed,SS4
1,104,204,5,739400,739.4,00:12:19.400,8200,8.2,3400,3.4,Completed,SS4
1,104,206,6,743100,743.1,00:12:23.100,11900,11.9,3700,3.7,Completed,SS4
1,105,205,1,828300,828.3,00:13:48.300,0,0.0,0,0.0,Completed,SS5
1,105,201,2,829700,829.7,00:13:49.700,1400,1.4,1400,1.4,Completed,SS5
1,105,203,3,831200,831.2,00:13:51.200,2900,2.9,1500,1.5,Completed,SS5
1,105,202,4,833800,833.8,00:13:53.800,5500,5.5,2600,2.6,Completed,SS5
1,105,204,5,836500,836.5,00:13:56.500,8200,8.2,2700,2.7,Completed,SS5
1,105,206,6,841000,841.0,00:14:01.000,12700,12.7,4500,4.5,Completed,SS5
````

## File: data/processed/rallye_automobile_monte_carlo_stages.csv
````
stage_id,stage_code,name,distance_km,surface,leg_name,status
101,SS1,Col de Turini,18.55,Tarmac,Leg 1,Completed
102,SS2,La Cabanette - Col de Braus,12.3,Tarmac,Leg 1,Completed
103,SS3,Lucéram - Lantosque,22.1,Tarmac,Leg 2,Completed
104,SS4,Saint-Léger - Escragnolles,15.8,Tarmac,Leg 2,Completed
105,SS5,Col de Turini (Power Stage),18.55,Tarmac,Leg 3,Completed
````

## File: docs/bloque-05-deploy.md
````markdown
# Bloque 5 — Pulido Final y Deploy

## Lecciones del Bloque 4

| Problema | Causa | Solucion |
|---|---|---|
| Bar chart sin nombres en eje Y | `tickvals`/`ticktext` no especificados, margen izquierdo de 10px | Añadir `tickmode="array"`, `margin=dict(l=180)` y `automargin=True` |
| Grouped bar chart mostraba solo una barra | Pandas Series con indice propio desalineaba los traces | Convertir a listas Python con `.tolist()` |
| Graficos con fondo blanco sobre tema oscuro | `plot_bgcolor="white"` no encaja con dark theme de Streamlit | `plot_bgcolor="rgba(0,0,0,0)"` + colores de texto/grid en blanco |

---

## Objetivo

Preparar el proyecto para produccion: configuracion de deploy, README final,
ajuste del `.gitignore` para incluir datos mock en el repo, y configuracion
de Streamlit Cloud + Render.

---

## Archivos creados / modificados

```
.gitignore                          <- modificado: CSVs mock incluidos, secrets excluidos
.streamlit/
    config.toml                     <- nuevo: tema dark + config servidor
    secrets.example.toml            <- nuevo: ejemplo de secrets para produccion
render.yaml                         <- nuevo: config de deploy en Render
dashboard/components/api_client.py  <- modificado: soporte Streamlit secrets
README.md                           <- modificado: version final con deploy
docs/bloque-05-deploy.md            <- este archivo
docs/contexto-proyecto.md           <- nuevo: contexto para futuras sesiones (en .gitignore)
docs/comandos.md                    <- nuevo: referencia rapida de comandos
```

---

## Configuracion de deploy

### Streamlit Cloud (dashboard)

Streamlit Cloud conecta directamente con el repo de GitHub y despliega con un click.

1. Ir a https://share.streamlit.io
2. New app → seleccionar repo `Rally-performance-analyzer`
3. Main file path: `dashboard/app.py`
4. En **Advanced settings → Secrets** añadir:
```toml
DASHBOARD_API_URL = "https://tu-api.onrender.com"
```
5. Deploy

El dashboard lee la URL de la API desde `st.secrets["DASHBOARD_API_URL"]` en produccion
y desde `os.getenv("DASHBOARD_API_URL", "http://localhost:8000")` en local.

### Render (FastAPI)

1. Ir a https://render.com → New Web Service
2. Conectar repo de GitHub
3. Configurar:
   - **Build command:** `pip install -r requirements.txt && WRC_USE_MOCK=true python -m ingestion.pipeline`
   - **Start command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11
4. Deploy

El `render.yaml` en la raiz del proyecto tambien permite deploy automatico.

### Nota sobre los datos en produccion

Los CSVs de mock (`data/processed/*.csv`) se incluyen en el repo (no estan en `.gitignore`)
para que el deploy funcione sin necesidad de ejecutar el pipeline. El build command
de Render los regenera igualmente como medida de seguridad.

---

## Cambios en .gitignore

| Cambio | Motivo |
|---|---|
| `data/processed/*.csv` → incluidos | Los CSVs de mock son pequeños y necesarios para el deploy |
| `repomix-output.md` → excluido | Archivo temporal de analisis, no pertenece al repo |
| `docs/contexto-proyecto.md` → excluido | Documento de uso personal, no publico |
| `.streamlit/secrets.toml` → excluido | Contiene URLs y credenciales de produccion |

---

## Streamlit theme

Configurado en `.streamlit/config.toml`:

| Parametro | Valor | Descripcion |
|---|---|---|
| `base` | `dark` | Tema oscuro base |
| `primaryColor` | `#C8102E` | Rojo Toyota (color primario del proyecto) |
| `backgroundColor` | `#0E1117` | Fondo principal |
| `secondaryBackgroundColor` | `#1A1A2E` | Fondo sidebar y cards |
| `textColor` | `#FAFAFA` | Texto principal |

---

## Validaciones del Bloque 5

### V1 — Tests siguen pasando
```bash
pytest backend/tests/ -v
→ 51 passed
```

### V2 — Dashboard arranca con tema correcto
```
streamlit run dashboard/app.py
→ Tema oscuro con color primario rojo visible
```

### V3 — .gitignore correcto
```bash
git status
→ data/processed/*.csv aparece como untracked (para anadir al repo)
→ repomix-output.md no aparece
→ docs/contexto-proyecto.md no aparece
```

### V4 — README final completo
```
README.md incluye: stack, funcionalidades, arquitectura,
instrucciones de ejecucion, instrucciones de deploy, tabla de estado
```

### V5 — Deploy en Streamlit Cloud
```
URL publica del dashboard funcionando
```

### V6 — Deploy en Render
```
URL publica de la API con /docs funcionando
```

---

## Commits sugeridos para cerrar el proyecto

```bash
# 1. Anadir CSVs de mock al repo
git add data/processed/
git commit -m "feat: include mock CSVs in repo for deploy"

# 2. Config de deploy y pulido final
git add .streamlit/ render.yaml .gitignore README.md
git add dashboard/components/api_client.py
git add docs/bloque-05-deploy.md docs/comandos.md
git commit -m "feat: bloque 5 - deploy config, Streamlit theme, README final"

# 3. Push
git push
```

---

## Posibles errores en deploy

| Error | Causa | Solucion |
|---|---|---|
| Dashboard no conecta con API | `DASHBOARD_API_URL` no configurado en secrets | Añadir en Streamlit Cloud secrets |
| Render falla en build | Python version incorrecta | Asegurar `PYTHON_VERSION=3.11.9` en env vars |
| `ModuleNotFoundError` en Render | PYTHONPATH no incluye root | Añadir `PYTHONPATH=.` en env vars de Render |
| CSVs no encontrados | Pipeline no se ejecuto en build | Verificar build command incluye `python -m ingestion.pipeline` |
````

## File: docs/comandos.md
````markdown
# Comandos de Referencia Rapida

Copia y pega directamente. Ejecutar siempre desde la raiz del proyecto.

---

## Setup inicial (solo la primera vez)

```bash
# Crear entorno virtual con Python 3.11
py -3.11 -m venv venv

# Activar entorno virtual
source venv/Scripts/activate        # Git Bash / Mac / Linux
# venv\Scripts\activate             # Windows CMD

# Instalar dependencias
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Copiar variables de entorno
cp .env.example .env
```

---

## Arranque del proyecto (cada vez)

```bash
# 0. Activar entorno virtual
source venv/Scripts/activate

# 1. Generar datos (solo si no existen en data/processed/)
WRC_USE_MOCK=true python -m ingestion.pipeline

# 2. Terminal 1 — Arrancar API
uvicorn backend.app.main:app --reload

# 3. Terminal 2 — Arrancar dashboard
streamlit run dashboard/app.py
```

URLs:
- Dashboard: http://localhost:8501
- API docs:  http://localhost:8000/docs
- API health: http://localhost:8000/health

---

## Tests

```bash
# Ejecutar todos los tests
pytest backend/tests/ -v

# Solo tests de API
pytest backend/tests/test_api.py -v

# Solo tests de ingesta
pytest backend/tests/test_ingestion.py -v
```

---

## Datos

```bash
# Regenerar todos los CSVs (modo mock)
rm data/processed/*.csv
WRC_USE_MOCK=true python -m ingestion.pipeline

# Verificar que los CSVs se leen correctamente
python -c "
import pandas as pd
files = [
    'data/processed/events.csv',
    'data/processed/rallye_automobile_monte_carlo_stages.csv',
    'data/processed/rallye_automobile_monte_carlo_entries.csv',
    'data/processed/rallye_automobile_monte_carlo_stage_times.csv',
    'data/processed/rallye_automobile_monte_carlo_overall.csv',
]
for f in files:
    df = pd.read_csv(f, encoding='utf-8-sig')
    print(f'OK: {f} ({len(df)} filas)')
"
```

---

## Git

```bash
# Ver estado
git status

# Commit
git add .
git commit -m "feat: descripcion del cambio"

# Push
git push

# Ver historial
git log --oneline
```

---

## Diagnostico de errores frecuentes

```bash
# Error: ModuleNotFoundError
# → Verificar que el venv esta activado
source venv/Scripts/activate
python --version   # debe ser 3.11.x

# Error: utf-8 codec can't decode
# → Regenerar CSVs con encoding correcto
rm data/processed/*.csv
WRC_USE_MOCK=true python -m ingestion.pipeline

# Error: No se puede conectar con la API
# → Verificar que uvicorn esta corriendo en terminal 1
curl http://localhost:8000/health

# Error: No module named 'dashboard'
# → Ejecutar streamlit desde la raiz del proyecto
# NO: cd dashboard && streamlit run app.py
# SI:  streamlit run dashboard/app.py
```

---

## Endpoints de la API

```bash
# Health
curl http://localhost:8000/health

# Rallies
curl http://localhost:8000/rallies/
curl http://localhost:8000/rallies/1

# Etapas
curl http://localhost:8000/stages/
curl http://localhost:8000/stages/101/times

# Pilotos
curl http://localhost:8000/drivers/
curl http://localhost:8000/drivers/classification
curl http://localhost:8000/drivers/evolution
curl "http://localhost:8000/drivers/compare?entry_a=201&entry_b=202"
```

---

## IDs de referencia (mock data)

| entry_id | Piloto | Fabricante | Coche |
|---|---|---|---|
| 201 | Sebastien Ogier | Toyota | #17 |
| 202 | Elfyn Evans | Toyota | #33 |
| 203 | Thierry Neuville | Hyundai | #11 |
| 204 | Ott Tanak | Hyundai | #6 |
| 205 | Kalle Rovanpera | Toyota | #69 |
| 206 | Ott Tanak | Hyundai | #8 |

| stage_id | Codigo | Nombre | Distancia |
|---|---|---|---|
| 101 | SS1 | Col de Turini | 18.55 km |
| 102 | SS2 | La Cabanette | 12.3 km |
| 103 | SS3 | Luceam | 22.1 km |
| 104 | SS4 | Saint-Leger | 15.8 km |
| 105 | SS5 | Power Stage | 18.55 km |
````

## File: render.yaml
````yaml
services:
  - type: web
    name: rally-performance-analyzer-api
    runtime: python
    buildCommand: pip install -r requirements.txt && WRC_USE_MOCK=true python -m ingestion.pipeline
    startCommand: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: WRC_USE_MOCK
        value: true
      - key: PYTHON_VERSION
        value: 3.11.9
````

## File: .env.example
````
# Copy this file to .env and fill in the values
# cp .env.example .env

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Dashboard
DASHBOARD_API_URL=http://localhost:8000

# Data paths (relative to project root)
DATA_RAW_PATH=data/raw
DATA_PROCESSED_PATH=data/processed

# WRC Data source
# true  → usa datos mock locales (desarrollo sin internet / red corporativa)
# false → llama a la API real de api.wrc.com
WRC_USE_MOCK=true
````

## File: .gitignore
````
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.eggs/

# Virtual environment
venv/
.venv/
env/

# Environment variables
.env
.env.local

# Data raw (JSON originales — regenerables, no subir)
data/raw/*.json
data/raw/*.csv

# Data processed — los CSVs de mock SI se suben al repo para el deploy
# Si quieres excluirlos, descomenta las siguientes lineas:
# data/processed/*.csv
# data/processed/*.parquet

# Keep the .gitkeep placeholders
!data/raw/.gitkeep
!data/processed/.gitkeep

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Repomix output (herramienta de analisis de codigo, no subir al repo)
repomix-output.md
repomix-output*.md

# Contexto interno del proyecto (uso personal, no subir al repo)
docs/contexto-proyecto.md

# Pytest
.pytest_cache/
.coverage
htmlcov/

# Streamlit secrets (contienen URLs y credenciales de produccion)
.streamlit/secrets.toml
````

## File: backend/__init__.py
````python

````

## File: backend/app/__init__.py
````python

````

## File: backend/app/config.py
````python
"""Application configuration loaded from environment variables."""

from pathlib import Path
from pydantic_settings import BaseSettings  # pydantic v2


class Settings(BaseSettings):
    # API server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Dashboard
    dashboard_api_url: str = "http://localhost:8000"

    # Paths (resolved relative to project root)
    data_raw_path: str = "data/raw"
    data_processed_path: str = "data/processed"

    @property
    def project_root(self) -> Path:
        """Absolute path to the project root (two levels up from this file)."""
        return Path(__file__).resolve().parents[2]

    @property
    def raw_dir(self) -> Path:
        return self.project_root / self.data_raw_path

    @property
    def processed_dir(self) -> Path:
        return self.project_root / self.data_processed_path

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
````

## File: backend/app/main.py
````python
"""Rally Performance Analyzer — FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routers import rally, stages, drivers

app = FastAPI(
    title="Rally Performance Analyzer",
    description="API para analizar datos del World Rally Championship.",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(rally.router)
app.include_router(stages.router)
app.include_router(drivers.router)


@app.get("/health", tags=["Status"])
def health_check() -> dict:
    """Endpoint de salud — confirma que la API está en marcha."""
    return {"status": "ok", "service": "rally-performance-analyzer"}
````

## File: backend/app/models/__init__.py
````python

````

## File: backend/app/models/schemas.py
````python
"""
Modelos Pydantic — esquemas de validación y serialización de la API.

Cada schema representa la estructura de datos que devuelven los endpoints.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Eventos ───────────────────────────────────────────────────────────────────

class EventSummary(BaseModel):
    """Resumen de un evento/rally."""
    event_id: int
    name: str
    status: str
    country: str
    country_iso: str
    date_start: str
    date_finish: str


# ── Etapas ────────────────────────────────────────────────────────────────────

class Stage(BaseModel):
    """Información de una etapa."""
    stage_id: int
    stage_code: str
    name: str
    distance_km: float
    surface: str
    leg_name: str
    status: str


# ── Pilotos ───────────────────────────────────────────────────────────────────

class Driver(BaseModel):
    """Información de un piloto inscrito."""
    entry_id: int
    driver_name: str
    driver_code: str
    driver_nationality: str
    codriver_name: str
    manufacturer: str
    car_number: str
    group: str


# ── Tiempos de etapa ──────────────────────────────────────────────────────────

class StageTimeEntry(BaseModel):
    """Tiempo de un piloto en una etapa concreta."""
    entry_id: int
    position: int
    time_s: float | None = None
    time_str: str | None = None
    diff_first_s: float | None = None
    diff_prev_s: float | None = None
    status: str
    # Enriquecido con datos del piloto
    driver_name: str = ""
    driver_code: str = ""
    manufacturer: str = ""
    car_number: str = ""


class StageResult(BaseModel):
    """Resultado completo de una etapa."""
    event_id: int
    stage_id: int
    stage_code: str
    entries: list[StageTimeEntry]


# ── Clasificación general ─────────────────────────────────────────────────────

class OverallEntry(BaseModel):
    """Posición de un piloto en la clasificación general."""
    entry_id: int
    position: int
    total_time_s: float | None = None
    total_time_str: str | None = None
    diff_first_s: float | None = None
    # Enriquecido
    driver_name: str = ""
    driver_code: str = ""
    manufacturer: str = ""
    car_number: str = ""


class OverallClassification(BaseModel):
    """Clasificación general tras una etapa."""
    event_id: int
    stage_id: int
    stage_code: str
    entries: list[OverallEntry]


# ── Comparativa entre pilotos ─────────────────────────────────────────────────

class DriverStageTime(BaseModel):
    """Tiempo de un piloto en una etapa para comparativa."""
    stage_code: str
    position: int
    time_s: float | None = None
    diff_first_s: float | None = None


class DriverComparison(BaseModel):
    """Comparativa de dos pilotos a lo largo del rally."""
    event_id: int
    driver_a: Driver
    driver_b: Driver
    stage_times_a: list[DriverStageTime]
    stage_times_b: list[DriverStageTime]


# ── Evolución de posiciones ───────────────────────────────────────────────────

class PositionAtStage(BaseModel):
    """Posición de un piloto tras cada etapa."""
    stage_code: str
    stage_id: int
    position: int
    total_time_s: float | None = None
    diff_first_s: float | None = None


class DriverEvolution(BaseModel):
    """Evolución de posición de un piloto a lo largo del rally."""
    entry_id: int
    driver_name: str
    driver_code: str
    manufacturer: str
    positions: list[PositionAtStage]
````

## File: backend/app/routers/__init__.py
````python

````

## File: backend/app/routers/drivers.py
````python
"""Router de pilotos — clasificación, evolución y comparativa."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from backend.app.models.schemas import (
    Driver,
    DriverComparison,
    DriverEvolution,
    DriverStageTime,
    OverallClassification,
    OverallEntry,
    PositionAtStage,
)
from backend.app.services import analytics, data_loader as loader
from backend.app.routers.stages import _isnan

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.get("/", response_model=list[Driver])
def list_drivers() -> list[Driver]:
    """Devuelve todos los pilotos inscritos en el rally."""
    df = loader.get_entries()
    if df.empty:
        return []
    return [
        Driver(
            entry_id=int(row["entry_id"]),
            driver_name=str(row["driver_name"]),
            driver_code=str(row.get("driver_code", "")),
            driver_nationality=str(row.get("driver_nationality", "")),
            codriver_name=str(row.get("codriver_name", "")),
            manufacturer=str(row.get("manufacturer", "")),
            car_number=str(row.get("car_number", "")),
            group=str(row.get("group", "")),
        )
        for _, row in df.iterrows()
    ]


@router.get("/classification", response_model=OverallClassification)
def get_final_classification() -> OverallClassification:
    """Devuelve la clasificación general final del rally."""
    df = analytics.get_final_classification()
    if df.empty:
        raise HTTPException(status_code=404, detail="No hay datos de clasificación")

    stages_df = loader.get_stages()
    last_stage_id = int(df.iloc[0]["stage_id"])
    stage_row = stages_df[stages_df["stage_id"] == last_stage_id]
    stage_code = str(stage_row.iloc[0]["stage_code"]) if not stage_row.empty else ""

    entries = [
        OverallEntry(
            entry_id=int(row["entry_id"]),
            position=int(row["position"]),
            total_time_s=float(row["total_time_s"]) if not _isnan(row.get("total_time_s")) else None,
            total_time_str=str(row.get("total_time_str", "")) or None,
            diff_first_s=float(row["diff_first_s"]) if not _isnan(row.get("diff_first_s")) else None,
            driver_name=str(row.get("driver_name", "")),
            driver_code=str(row.get("driver_code", "")),
            manufacturer=str(row.get("manufacturer", "")),
            car_number=str(row.get("car_number", "")),
        )
        for _, row in df.iterrows()
    ]

    return OverallClassification(
        event_id=int(df.iloc[0]["event_id"]),
        stage_id=last_stage_id,
        stage_code=stage_code,
        entries=entries,
    )


@router.get("/evolution", response_model=list[DriverEvolution])
def get_all_evolution() -> list[DriverEvolution]:
    """Devuelve la evolución de posición de todos los pilotos (bump chart)."""
    df = analytics.get_all_drivers_evolution()
    if df.empty:
        return []

    result = []
    for entry_id, group in df.groupby("entry_id"):
        row0 = group.iloc[0]
        positions = [
            PositionAtStage(
                stage_code=str(r.get("stage_code", "")),
                stage_id=int(r["stage_id"]),
                position=int(r["position"]),
                total_time_s=float(r["total_time_s"]) if not _isnan(r.get("total_time_s")) else None,
                diff_first_s=float(r["diff_first_s"]) if not _isnan(r.get("diff_first_s")) else None,
            )
            for _, r in group.iterrows()
        ]
        result.append(DriverEvolution(
            entry_id=int(entry_id),
            driver_name=str(row0.get("driver_name", "")),
            driver_code=str(row0.get("driver_code", "")),
            manufacturer=str(row0.get("manufacturer", "")),
            positions=positions,
        ))

    return result


@router.get("/compare", response_model=DriverComparison)
def compare_drivers(
    entry_a: int = Query(..., description="entry_id del piloto A"),
    entry_b: int = Query(..., description="entry_id del piloto B"),
) -> DriverComparison:
    """Compara los tiempos por etapa de dos pilotos."""
    entries_df = loader.get_entries()

    def _get_driver(entry_id: int) -> Driver:
        row = entries_df[entries_df["entry_id"] == entry_id]
        if row.empty:
            raise HTTPException(status_code=404, detail=f"Piloto {entry_id} no encontrado")
        r = row.iloc[0]
        return Driver(
            entry_id=int(r["entry_id"]),
            driver_name=str(r["driver_name"]),
            driver_code=str(r.get("driver_code", "")),
            driver_nationality=str(r.get("driver_nationality", "")),
            codriver_name=str(r.get("codriver_name", "")),
            manufacturer=str(r.get("manufacturer", "")),
            car_number=str(r.get("car_number", "")),
            group=str(r.get("group", "")),
        )

    driver_a = _get_driver(entry_a)
    driver_b = _get_driver(entry_b)

    data = analytics.get_driver_comparison(entry_a, entry_b)

    def _to_stage_times(df) -> list[DriverStageTime]:
        return [
            DriverStageTime(
                stage_code=str(r.get("stage_code", "")),
                position=int(r["position"]),
                time_s=float(r["time_s"]) if not _isnan(r.get("time_s")) else None,
                diff_first_s=float(r["diff_first_s"]) if not _isnan(r.get("diff_first_s")) else None,
            )
            for _, r in df.iterrows()
        ]

    return DriverComparison(
        event_id=1,
        driver_a=driver_a,
        driver_b=driver_b,
        stage_times_a=_to_stage_times(data["driver_a"]),
        stage_times_b=_to_stage_times(data["driver_b"]),
    )
````

## File: backend/app/routers/rally.py
````python
"""Router de rally — endpoints de eventos y información general."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.models.schemas import EventSummary
from backend.app.services import data_loader as loader

router = APIRouter(prefix="/rallies", tags=["Rallies"])


@router.get("/", response_model=list[EventSummary])
def list_rallies() -> list[EventSummary]:
    """Devuelve todos los rallies de la temporada activa."""
    df = loader.get_events()
    if df.empty:
        return []
    return [
        EventSummary(
            event_id=int(row["event_id"]),
            name=str(row["name"]),
            status=str(row["status"]),
            country=str(row["country"]),
            country_iso=str(row.get("country_iso", "")),
            date_start=str(row.get("date_start", "")),
            date_finish=str(row.get("date_finish", "")),
        )
        for _, row in df.iterrows()
    ]


@router.get("/{event_id}", response_model=EventSummary)
def get_rally(event_id: int) -> EventSummary:
    """Devuelve la información de un rally concreto."""
    df = loader.get_events()
    row = df[df["event_id"] == event_id]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Rally {event_id} no encontrado")
    r = row.iloc[0]
    return EventSummary(
        event_id=int(r["event_id"]),
        name=str(r["name"]),
        status=str(r["status"]),
        country=str(r["country"]),
        country_iso=str(r.get("country_iso", "")),
        date_start=str(r.get("date_start", "")),
        date_finish=str(r.get("date_finish", "")),
    )
````

## File: backend/app/routers/stages.py
````python
"""Router de etapas — endpoints de etapas y tiempos."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.models.schemas import Stage, StageResult, StageTimeEntry
from backend.app.services import analytics, data_loader as loader

router = APIRouter(prefix="/stages", tags=["Stages"])


@router.get("/", response_model=list[Stage])
def list_stages() -> list[Stage]:
    """Devuelve todas las etapas del rally."""
    df = loader.get_stages()
    if df.empty:
        return []
    return [
        Stage(
            stage_id=int(row["stage_id"]),
            stage_code=str(row["stage_code"]),
            name=str(row["name"]),
            distance_km=float(row["distance_km"]),
            surface=str(row["surface"]),
            leg_name=str(row.get("leg_name", "")),
            status=str(row.get("status", "")),
        )
        for _, row in df.iterrows()
    ]


@router.get("/{stage_id}/times", response_model=StageResult)
def get_stage_times(stage_id: int) -> StageResult:
    """Devuelve los tiempos de todos los pilotos en una etapa concreta."""
    stages_df = loader.get_stages()
    stage_row = stages_df[stages_df["stage_id"] == stage_id]
    if stage_row.empty:
        raise HTTPException(status_code=404, detail=f"Etapa {stage_id} no encontrada")

    stage_code = str(stage_row.iloc[0]["stage_code"])
    df = analytics.get_stage_result(stage_id)

    entries = [
        StageTimeEntry(
            entry_id=int(row["entry_id"]),
            position=int(row["position"]),
            time_s=float(row["time_s"]) if not _isnan(row.get("time_s")) else None,
            time_str=str(row["time_str"]) if row.get("time_str") else None,
            diff_first_s=float(row["diff_first_s"]) if not _isnan(row.get("diff_first_s")) else None,
            diff_prev_s=float(row["diff_prev_s"]) if not _isnan(row.get("diff_prev_s")) else None,
            status=str(row.get("status", "")),
            driver_name=str(row.get("driver_name", "")),
            driver_code=str(row.get("driver_code", "")),
            manufacturer=str(row.get("manufacturer", "")),
            car_number=str(row.get("car_number", "")),
        )
        for _, row in df.iterrows()
    ]

    return StageResult(
        event_id=int(df.iloc[0]["event_id"]) if not df.empty else 0,
        stage_id=stage_id,
        stage_code=stage_code,
        entries=entries,
    )


def _isnan(val) -> bool:
    """Comprueba si un valor es NaN de forma segura."""
    try:
        import math
        return math.isnan(float(val))
    except (TypeError, ValueError):
        return val is None
````

## File: backend/app/services/__init__.py
````python

````

## File: backend/tests/__init__.py
````python

````

## File: backend/tests/test_api.py
````python
"""
Tests del Bloque 2 — Endpoints FastAPI.

Usa TestClient con datos reales de los CSVs generados en el Bloque 1.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.data_loader import clear_cache

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_cache():
    """Limpia la caché antes de cada test para evitar contaminación."""
    clear_cache()
    yield
    clear_cache()


# ── /health ───────────────────────────────────────────────────────────────────

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── /rallies ──────────────────────────────────────────────────────────────────

def test_list_rallies_status():
    r = client.get("/rallies/")
    assert r.status_code == 200

def test_list_rallies_returns_list():
    r = client.get("/rallies/")
    assert isinstance(r.json(), list)

def test_list_rallies_not_empty():
    r = client.get("/rallies/")
    assert len(r.json()) > 0

def test_get_rally_by_id():
    r = client.get("/rallies/1")
    assert r.status_code == 200
    data = r.json()
    assert data["event_id"] == 1
    assert "name" in data

def test_get_rally_not_found():
    r = client.get("/rallies/9999")
    assert r.status_code == 404

def test_rally_has_required_fields():
    r = client.get("/rallies/1")
    data = r.json()
    for field in ["event_id", "name", "status", "country"]:
        assert field in data


# ── /stages ───────────────────────────────────────────────────────────────────

def test_list_stages_status():
    r = client.get("/stages/")
    assert r.status_code == 200

def test_list_stages_count():
    r = client.get("/stages/")
    assert len(r.json()) == 5  # SS1-SS5

def test_stage_has_required_fields():
    r = client.get("/stages/")
    stage = r.json()[0]
    for field in ["stage_id", "stage_code", "name", "distance_km", "surface"]:
        assert field in stage

def test_get_stage_times_status():
    r = client.get("/stages/101/times")
    assert r.status_code == 200

def test_get_stage_times_has_entries():
    r = client.get("/stages/101/times")
    data = r.json()
    assert "entries" in data
    assert len(data["entries"]) == 6

def test_get_stage_times_first_position():
    r = client.get("/stages/101/times")
    entries = r.json()["entries"]
    positions = [e["position"] for e in entries]
    assert 1 in positions

def test_get_stage_times_has_driver_name():
    r = client.get("/stages/101/times")
    entry = r.json()["entries"][0]
    assert entry["driver_name"] != ""

def test_get_stage_times_not_found():
    r = client.get("/stages/9999/times")
    assert r.status_code == 404


# ── /drivers ──────────────────────────────────────────────────────────────────

def test_list_drivers_status():
    r = client.get("/drivers/")
    assert r.status_code == 200

def test_list_drivers_count():
    r = client.get("/drivers/")
    assert len(r.json()) == 6

def test_driver_has_required_fields():
    r = client.get("/drivers/")
    driver = r.json()[0]
    for field in ["entry_id", "driver_name", "manufacturer", "car_number"]:
        assert field in driver


# ── /drivers/classification ───────────────────────────────────────────────────

def test_classification_status():
    r = client.get("/drivers/classification")
    assert r.status_code == 200

def test_classification_has_entries():
    r = client.get("/drivers/classification")
    data = r.json()
    assert "entries" in data
    assert len(data["entries"]) == 6

def test_classification_leader_gap_zero():
    r = client.get("/drivers/classification")
    leader = r.json()["entries"][0]
    assert leader["position"] == 1
    assert leader["diff_first_s"] == 0.0

def test_classification_has_driver_info():
    r = client.get("/drivers/classification")
    leader = r.json()["entries"][0]
    assert leader["driver_name"] != ""
    assert leader["manufacturer"] != ""


# ── /drivers/evolution ────────────────────────────────────────────────────────

def test_evolution_status():
    r = client.get("/drivers/evolution")
    assert r.status_code == 200

def test_evolution_all_drivers():
    r = client.get("/drivers/evolution")
    assert len(r.json()) == 6

def test_evolution_has_positions():
    r = client.get("/drivers/evolution")
    driver = r.json()[0]
    assert "positions" in driver
    assert len(driver["positions"]) == 5  # 5 etapas


# ── /drivers/compare ──────────────────────────────────────────────────────────

def test_compare_status():
    r = client.get("/drivers/compare?entry_a=201&entry_b=202")
    assert r.status_code == 200

def test_compare_has_both_drivers():
    r = client.get("/drivers/compare?entry_a=201&entry_b=202")
    data = r.json()
    assert "driver_a" in data
    assert "driver_b" in data

def test_compare_has_stage_times():
    r = client.get("/drivers/compare?entry_a=201&entry_b=202")
    data = r.json()
    assert len(data["stage_times_a"]) == 5
    assert len(data["stage_times_b"]) == 5

def test_compare_driver_not_found():
    r = client.get("/drivers/compare?entry_a=201&entry_b=9999")
    assert r.status_code == 404
````

## File: backend/tests/test_health.py
````python
"""Tests del Bloque 0 — verificación básica de la API."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_check_status_200():
    """El endpoint /health debe devolver 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_body():
    """El endpoint /health debe devolver status ok."""
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "rally-performance-analyzer"


def test_docs_available():
    """Swagger UI debe estar disponible en /docs."""
    response = client.get("/docs")
    assert response.status_code == 200
````

## File: backend/tests/test_ingestion.py
````python
"""
Tests del Bloque 1 — Ingesta de datos.

Validan los transformadores con datos de ejemplo (sin llamar a la API real).
"""

import pandas as pd
import pytest

from ingestion.transformers import (
    transform_entries,
    transform_events,
    transform_overall_results,
    transform_stage_times,
    transform_stages,
    _ms_to_seconds,
    _ms_to_timestr,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def test_ms_to_seconds_basic():
    assert _ms_to_seconds(90000) == 90.0

def test_ms_to_seconds_precision():
    assert _ms_to_seconds(90500) == 90.5

def test_ms_to_seconds_none():
    assert _ms_to_seconds(None) is None

def test_ms_to_timestr_basic():
    # 1 minuto 30 segundos = 90000 ms
    assert _ms_to_timestr(90000) == "00:01:30.000"

def test_ms_to_timestr_none():
    assert _ms_to_timestr(None) is None


# ── Eventos ───────────────────────────────────────────────────────────────────

MOCK_EVENTS = [
    {
        "id": 1,
        "name": "Rally Monte Carlo",
        "status": "Completed",
        "rally": {
            "country": {"name": "France", "iso2": "FR"}
        },
        "eventDays": [
            {"startDate": "2024-01-25"},
            {"finishDate": "2024-01-28"},
        ],
    }
]

def test_transform_events_columns():
    df = transform_events(MOCK_EVENTS)
    assert "event_id" in df.columns
    assert "name" in df.columns
    assert "country" in df.columns

def test_transform_events_values():
    df = transform_events(MOCK_EVENTS)
    assert df.iloc[0]["event_id"] == 1
    assert df.iloc[0]["name"] == "Rally Monte Carlo"
    assert df.iloc[0]["country"] == "France"

def test_transform_events_empty():
    df = transform_events([])
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


# ── Etapas ────────────────────────────────────────────────────────────────────

MOCK_ITINERARY = {
    "itineraryLegs": [
        {
            "name": "Leg 1",
            "itinerarySections": [
                {
                    "stages": [
                        {
                            "stageId": 101,
                            "code": "SS1",
                            "name": "Col de Turini",
                            "distance": 18.5,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                        {
                            "stageId": 102,
                            "code": "SS2",
                            "name": "La Cabanette",
                            "distance": 12.3,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                    ]
                }
            ],
        }
    ]
}

def test_transform_stages_count():
    df = transform_stages(MOCK_ITINERARY)
    assert len(df) == 2

def test_transform_stages_columns():
    df = transform_stages(MOCK_ITINERARY)
    assert "stage_id" in df.columns
    assert "stage_code" in df.columns
    assert "distance_km" in df.columns

def test_transform_stages_values():
    df = transform_stages(MOCK_ITINERARY)
    assert df.iloc[0]["stage_code"] == "SS1"
    assert df.iloc[0]["distance_km"] == 18.5


# ── Pilotos ───────────────────────────────────────────────────────────────────

MOCK_ENTRIES = [
    {
        "entryId": 201,
        "identifier": "1",
        "driver": {
            "fullName": "Sébastien Ogier",
            "code": "OGI",
            "country": {"iso2": "FR"},
        },
        "codriver": {"fullName": "Vincent Landais"},
        "manufacturer": {"name": "Toyota"},
        "group": {"name": "WRC"},
    }
]

def test_transform_entries_columns():
    df = transform_entries(MOCK_ENTRIES)
    assert "entry_id" in df.columns
    assert "driver_name" in df.columns
    assert "manufacturer" in df.columns

def test_transform_entries_values():
    df = transform_entries(MOCK_ENTRIES)
    assert df.iloc[0]["driver_name"] == "Sébastien Ogier"
    assert df.iloc[0]["manufacturer"] == "Toyota"
    assert df.iloc[0]["car_number"] == "1"


# ── Tiempos de etapa ──────────────────────────────────────────────────────────

MOCK_STAGE_TIMES = [
    {
        "entryId": 201,
        "position": 1,
        "elapsedDurationMs": 834500,
        "diffFirstMs": 0,
        "diffPrevMs": 0,
        "status": "Completed",
    },
    {
        "entryId": 202,
        "position": 2,
        "elapsedDurationMs": 835500,
        "diffFirstMs": 1000,
        "diffPrevMs": 1000,
        "status": "Completed",
    },
]

def test_transform_stage_times_count():
    df = transform_stage_times(MOCK_STAGE_TIMES, stage_id=101, event_id=1)
    assert len(df) == 2

def test_transform_stage_times_columns():
    df = transform_stage_times(MOCK_STAGE_TIMES, stage_id=101, event_id=1)
    assert "time_s" in df.columns
    assert "diff_first_s" in df.columns
    assert "time_str" in df.columns

def test_transform_stage_times_conversion():
    df = transform_stage_times(MOCK_STAGE_TIMES, stage_id=101, event_id=1)
    assert df.iloc[0]["time_s"] == 834.5
    assert df.iloc[1]["diff_first_s"] == 1.0

def test_transform_stage_times_sorted():
    """Los tiempos deben estar ordenados por posición."""
    df = transform_stage_times(MOCK_STAGE_TIMES, stage_id=101, event_id=1)
    assert df.iloc[0]["position"] == 1
    assert df.iloc[1]["position"] == 2


# ── Clasificación general ─────────────────────────────────────────────────────

MOCK_OVERALL = [
    {
        "entryId": 201,
        "position": 1,
        "totalTimeMs": 5000000,
        "diffFirstMs": 0,
        "penaltyTimeMs": 0,
    },
    {
        "entryId": 202,
        "position": 2,
        "totalTimeMs": 5015000,
        "diffFirstMs": 15000,
        "penaltyTimeMs": 0,
    },
]

def test_transform_overall_results_count():
    df = transform_overall_results(MOCK_OVERALL, stage_id=101, event_id=1)
    assert len(df) == 2

def test_transform_overall_results_leader_gap():
    df = transform_overall_results(MOCK_OVERALL, stage_id=101, event_id=1)
    assert df.iloc[0]["diff_first_s"] == 0.0
    assert df.iloc[1]["diff_first_s"] == 15.0
````

## File: conftest.py
````python

````

## File: dashboard/components/api_client.py
````python
from __future__ import annotations
import logging
import os
import requests

logger = logging.getLogger(__name__)


def _get_api_base() -> str:
    """Obtiene la URL base de la API segun el entorno."""
    try:
        from pathlib import Path
        import streamlit as st
        # Streamlit emite "No secrets files found" al acceder a st.secrets aunque
        # el archivo no exista. Comprobamos las mismas rutas que usa internamente
        # y solo leemos secrets si el archivo existe, evitando el warning.
        _secrets_paths = (
            Path.home() / ".streamlit" / "secrets.toml",
            Path(".streamlit") / "secrets.toml",
        )
        if any(p.exists() for p in _secrets_paths):
            url = st.secrets.get("DASHBOARD_API_URL", None)
            if url:
                return url
    except Exception:
        pass
    return os.getenv("DASHBOARD_API_URL", "http://localhost:8000")


def _get(path: str, params: dict | None = None) -> dict | list | None:
    url = f"{_get_api_base()}{path}"
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        logger.error("No se puede conectar con la API en %s", _get_api_base())
        return None
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error %s en %s", e.response.status_code, url)
        return None


def get_rallies() -> list[dict]:
    return _get("/rallies/") or []

def get_rally(event_id: int) -> dict | None:
    return _get(f"/rallies/{event_id}")

def get_stages() -> list[dict]:
    return _get("/stages/") or []

def get_stage_times(stage_id: int) -> dict | None:
    return _get(f"/stages/{stage_id}/times")

def get_drivers() -> list[dict]:
    return _get("/drivers/") or []

def get_classification() -> dict | None:
    return _get("/drivers/classification")

def get_evolution() -> list[dict]:
    return _get("/drivers/evolution") or []

def compare_drivers(entry_a: int, entry_b: int) -> dict | None:
    return _get("/drivers/compare", params={"entry_a": entry_a, "entry_b": entry_b})
````

## File: data/processed/.gitkeep
````

````

## File: data/raw/.gitkeep
````

````

## File: docs/bloque-00-setup.md
````markdown
# Bloque 0 — Setup del Proyecto

## Objetivo

Crear la estructura base del proyecto, configurar el entorno de desarrollo y
verificar que FastAPI y Streamlit arrancan correctamente.

---

## Estructura de carpetas creada

```
rally-performance-analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app + CORS + /health
│   │   ├── config.py        # Settings con pydantic-settings
│   │   ├── models/          # (vacío — se rellena en Bloque 2)
│   │   ├── routers/         # (vacío — se rellena en Bloque 2)
│   │   └── services/        # (vacío — se rellena en Bloque 2)
│   └── tests/
│       ├── __init__.py
│       └── test_health.py   # 3 tests básicos del /health
├── data/
│   ├── raw/                 # JSON descargados de la WRC API (Bloque 1)
│   └── processed/           # CSV/Parquet limpios (Bloque 1)
├── ingestion/
│   └── __init__.py          # (se rellena en Bloque 1)
├── dashboard/
│   └── app.py               # Streamlit hello-world con métricas placeholder
├── docs/
│   └── bloque-00-setup.md   # Este archivo
├── .env.example
├── .gitignore
├── Makefile
├── pytest.ini
└── requirements.txt
```

---

## Archivos clave

### `requirements.txt`

Dependencias con versiones fijadas para reproducibilidad:

| Paquete | Versión | Uso |
|---|---|---|
| fastapi | 0.111.0 | Framework backend |
| uvicorn | 0.29.0 | Servidor ASGI |
| streamlit | 1.35.0 | Dashboard |
| pandas | 2.2.2 | Procesamiento de datos |
| plotly | 5.22.0 | Visualización |
| httpx | 0.27.0 | Cliente HTTP (WRC API) |
| pydantic | 2.7.1 | Validación de modelos |
| pytest | 8.2.0 | Tests |
| python-dotenv | 1.0.1 | Variables de entorno |

### `backend/app/main.py`

- Crea la instancia de FastAPI con título, descripción y versión.
- Añade middleware CORS para permitir llamadas desde Streamlit.
- Define el endpoint `GET /health` que devuelve `{"status": "ok"}`.

### `backend/app/config.py`

- Usa `pydantic-settings` para cargar variables desde `.env`.
- Expone propiedades `raw_dir` y `processed_dir` como rutas absolutas.
- Se usa en todos los bloques siguientes para acceder a los paths de datos.

### `dashboard/app.py`

- Página inicial de Streamlit con layout wide.
- Muestra el estado de cada bloque con `st.metric` como placeholders.

### `Makefile`

| Comando | Acción |
|---|---|
| `make install` | Crea venv e instala dependencias |
| `make run-api` | Arranca FastAPI en `localhost:8000` |
| `make run-dashboard` | Arranca Streamlit en `localhost:8501` |
| `make test` | Ejecuta pytest |

---

## Cómo arrancar

```bash
# 1. Crear entorno virtual e instalar dependencias
make install

# 2. Activar el entorno virtual
source venv/bin/activate   # Linux/Mac
# o en Windows:
# venv\Scripts\activate

# 3. Arrancar la API (terminal 1)
make run-api

# 4. Arrancar el dashboard (terminal 2)
make run-dashboard
```

---

## Validaciones del Bloque 0

### V1 — FastAPI arranca
```
http://localhost:8000/health
→ {"status": "ok", "service": "rally-performance-analyzer"}
```

### V2 — Swagger disponible
```
http://localhost:8000/docs
→ Interfaz Swagger UI visible en el navegador
```

### V3 — Streamlit arranca
```
http://localhost:8501
→ Dashboard visible con título "🏁 Rally Performance Analyzer"
```

### V4 — Tests pasan
```bash
make test
→ 3 passed
```

---

## Posibles errores comunes

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: pydantic_settings` | Falta instalar | `pip install pydantic-settings` |
| `address already in use :8000` | Puerto ocupado | `lsof -i :8000` y matar el proceso |
| `address already in use :8501` | Puerto ocupado | `lsof -i :8501` y matar el proceso |
| Tests fallan con `ModuleNotFoundError` | pytest no ve el root | Ejecutar desde la raíz del proyecto |

---

*Siguiente: Bloque 1 — Ingesta de datos desde la WRC API.*
````

## File: docs/bloque-01-ingesta.md
````markdown
# Bloque 1 — Ingesta de Datos WRC

## Lecciones del Bloque 0

Problemas reales encontrados durante el Bloque 0:

| Problema | Causa | Solución |
|---|---|---|
| `pip install` falla con `pydantic-core` / `pillow` | Python 3.14 sin wheels precompilados | Usar Python 3.11 (`py -3.11 -m venv venv`) |
| `SSLError: CERTIFICATE_VERIFY_FAILED` | Red corporativa con proxy | `pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org` |
| `ModuleNotFoundError: No module named 'backend'` | pytest no encuentra el root | Crear `conftest.py` vacío en raíz + `backend/__init__.py` |

---

## Objetivo

Conectar con la WRC Live Timing API, descargar datos reales de un rally completo,
limpiarlos con Pandas y guardarlos en `data/processed/` como CSVs listos para usar.

---

## Problema encontrado: api.wrc.com ya no existe

Durante el desarrollo de este bloque se descubrió que **`api.wrc.com` ha dejado de funcionar**.

### Diagnóstico

- Error en Python: `httpx.ConnectError: [Errno 11001] getaddrinfo failed`
- Error en navegador: `DNS_PROBE_FINISHED_NXDOMAIN`
- Verificado desde servidor externo (no es la red corporativa): `curl: (6) Could not resolve host: api.wrc.com`

**Conclusión: el dominio `api.wrc.com` ha sido dado de baja por WRC.** La API era no oficial y dependía de la infraestructura interna del WRC Live Timing, que ha cambiado.

### Decisión: Mock Data

Se optó por crear datos mock realistas en lugar de buscar un scraper alternativo. Motivos:

1. Para un proyecto de portfolio lo que importa es la **arquitectura y los gráficos**, no la fuente exacta de los datos.
2. Los datos mock siguen la **estructura idéntica** a la API real (mismos campos, mismos tipos).
3. En una entrevista se puede explicar con total transparencia: *"La API original dejó de estar disponible, así que construí datos mock con la misma estructura para poder demostrar el pipeline completo."*

---

## Cómo está construido el mock

El fichero `ingestion/mock_data.py` simula el **Rally Monte Carlo 2024** con datos verosímiles:

### Estructura

| Dataset | Contenido |
|---|---|
| `MOCK_SEASON` | 3 eventos (Monte Carlo, Sweden, Kenya) con estado `Completed` |
| `MOCK_ITINERARY` | 3 legs, 5 etapas (SS1-SS5) con distancias reales |
| `MOCK_ENTRIES` | 6 pilotos reales: Ogier, Evans, Neuville, Tänak, Rovanperä + 1 |
| `MOCK_STAGE_TIMES` | Tiempos por etapa para los 6 pilotos, en milisegundos |
| `MOCK_OVERALL` | Clasificación acumulada tras cada etapa |

### Criterios de realismo

- Tiempos basados en **ritmo real del WRC en tarmac (~1 min/km)**
- SS1 (18.55 km) → ~834 segundos (13:54) para el ganador
- Gaps entre pilotos de 1-3 segundos por etapa (valores reales del WRC)
- Los líderes de etapa varían (no siempre gana el mismo piloto)
- La clasificación general evoluciona de forma coherente

### Control del modo mock

```bash
# Activar mock (desarrollo / red corporativa)
WRC_USE_MOCK=true python -m ingestion.pipeline

# Desactivar mock (cuando la API real esté disponible)
WRC_USE_MOCK=false python -m ingestion.pipeline
```

También se puede configurar en el `.env`:
```
WRC_USE_MOCK=true
```

---

## Archivos creados

```
ingestion/
├── __init__.py
├── wrc_client.py      # Cliente HTTP con soporte mock/real
├── mock_data.py       # Datos mock del Rally Monte Carlo 2024
├── transformers.py    # Limpieza y normalización con Pandas
└── pipeline.py        # Orquestador — descarga y guarda todo

backend/tests/
└── test_ingestion.py  # 19 tests de los transformadores
```

---

## Arquitectura de la ingesta

```
WRC API (o mock_data.py)
        │
        ▼
wrc_client.py          → llamadas HTTP con httpx (o datos mock)
        │  JSON crudo
        ▼
transformers.py        → limpieza, normalización, conversión ms→s
        │  DataFrames
        ▼
pipeline.py            → orquesta y guarda en data/raw/ y data/processed/
        │
        ├── data/raw/          JSON originales (trazabilidad)
        └── data/processed/    CSVs limpios (usados por FastAPI)
```

---

## Módulos

### `wrc_client.py`

Cliente HTTP con modo dual (real/mock):

| Función | Descripción |
|---|---|
| `get_active_season()` | Lista de eventos de la temporada |
| `get_itinerary(event_id)` | Legs, sections y stages |
| `get_entries(event_id)` | Pilotos inscritos |
| `get_stage_times(event_id, stage_id)` | Tiempos de una etapa |
| `get_overall_results(event_id, stage_id)` | Clasificación acumulada |

### `transformers.py`

Funciones puras que devuelven DataFrames limpios:

| Función | Output CSV |
|---|---|
| `transform_events()` | `events.csv` |
| `transform_stages()` | `*_stages.csv` |
| `transform_entries()` | `*_entries.csv` |
| `transform_stage_times()` | `*_stage_times.csv` |
| `transform_overall_results()` | `*_overall.csv` |

Conversiones aplicadas:
- `elapsedDurationMs` → `time_s` (float) y `time_str` (HH:MM:SS.mmm)
- `diffFirstMs` → `diff_first_s`
- Ordenación por `position`
- Casting de IDs a `int`

---

## CSVs generados

Tras ejecutar el pipeline se crean en `data/processed/`:

```
events.csv                                   (3 filas)
rallye_automobile_monte_carlo_stages.csv     (5 filas)
rallye_automobile_monte_carlo_entries.csv    (6 filas)
rallye_automobile_monte_carlo_stage_times.csv (30 filas = 5 etapas × 6 pilotos)
rallye_automobile_monte_carlo_overall.csv    (30 filas = 5 etapas × 6 pilotos)
```

---

## Lecciones del Bloque 1

| Problema | Causa | Solución |
|---|---|---|
| `api.wrc.com` no resuelve | Dominio dado de baja por WRC | Mock data con estructura idéntica |
| `WRC_USE_MOCK` no se lee desde `.env` | `load_dotenv()` se ejecuta después de que `os.getenv()` ya se evaluó | Pasar la variable directamente: `WRC_USE_MOCK=true python -m ingestion.pipeline` |
| Archivos del zip no reemplazan los existentes | Windows no sobreescribe al descomprimir si no se confirma | Confirmar sobreescritura al descomprimir, o copiar archivos manualmente |

---

## Validaciones completadas

```
V1 — 22/22 tests passed              ✅
V2 — Pipeline ejecutado con mock     ✅
V3 — events.csv generado             ✅
V4 — *_stages.csv generado           ✅
V5 — *_stage_times.csv generado      ✅
V6 — *_overall.csv generado          ✅
```

---

*Siguiente: Bloque 2 — Backend FastAPI con endpoints REST.*
````

## File: docs/bloque-02-backend.md
````markdown
# Bloque 2 — Backend FastAPI

## Lecciones del Bloque 1

| Problema | Causa | Solución |
|---|---|---|
| `api.wrc.com` no resuelve | Dominio dado de baja por WRC | Mock data con estructura idéntica |
| `WRC_USE_MOCK` no se lee desde `.env` | `os.getenv()` se evalúa antes de `load_dotenv()` | Pasar la variable inline: `WRC_USE_MOCK=true python -m ingestion.pipeline` |
| Archivos del zip no reemplazan los existentes | Windows no sobreescribe sin confirmación | Copiar archivos manualmente en VSCode |

---

## Objetivo

Construir el backend REST con FastAPI que expone los datos procesados del Bloque 1
como endpoints JSON, con validación Pydantic, documentación Swagger automática y tests.

---

## Archivos creados / modificados

```
backend/
├── app/
│   ├── main.py                    ← modificado: añadidos los 3 routers
│   ├── models/
│   │   └── schemas.py             ← nuevo: todos los modelos Pydantic
│   ├── services/
│   │   ├── data_loader.py         ← nuevo: carga y caché de CSVs
│   │   └── analytics.py          ← nuevo: lógica de negocio
│   └── routers/
│       ├── rally.py               ← nuevo: endpoints de eventos
│       ├── stages.py              ← nuevo: endpoints de etapas
│       └── drivers.py             ← nuevo: endpoints de pilotos
└── tests/
    └── test_api.py                ← nuevo: 35 tests de endpoints

requirements.txt                   ← añadido pydantic-settings==2.3.0
```

---

## Arquitectura del backend

```
CSV (data/processed/)
        │
        ▼
data_loader.py      → carga DataFrames con lru_cache (singleton)
        │
        ▼
analytics.py        → cálculos: clasificación final, evolución, comparativa
        │
        ▼
routers/            → endpoints REST con validación Pydantic
        │
        ▼
Swagger /docs       → documentación automática
```

---

## Endpoints disponibles

### Status
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado de la API |

### Rallies
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/rallies/` | Lista de todos los rallies de la temporada |
| GET | `/rallies/{event_id}` | Detalle de un rally concreto |

### Stages
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/stages/` | Lista de todas las etapas |
| GET | `/stages/{stage_id}/times` | Tiempos de todos los pilotos en una etapa |

### Drivers
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/drivers/` | Lista de pilotos inscritos |
| GET | `/drivers/classification` | Clasificación general final |
| GET | `/drivers/evolution` | Evolución de posición de todos los pilotos |
| GET | `/drivers/compare?entry_a=X&entry_b=Y` | Comparativa entre dos pilotos |

---

## Modelos Pydantic (schemas.py)

| Schema | Descripción |
|---|---|
| `EventSummary` | Resumen de un rally (id, nombre, país, fechas) |
| `Stage` | Etapa (id, código, nombre, distancia, superficie) |
| `Driver` | Piloto (id, nombre, copiloto, fabricante, número) |
| `StageTimeEntry` | Tiempo de un piloto en una etapa con datos enriquecidos |
| `StageResult` | Resultado completo de una etapa (lista de StageTimeEntry) |
| `OverallEntry` | Posición en clasificación general |
| `OverallClassification` | Clasificación general completa |
| `DriverEvolution` | Evolución de posición etapa a etapa |
| `DriverComparison` | Comparativa de tiempos entre dos pilotos |

---

## Servicios

### `data_loader.py`
- Carga los CSVs de `data/processed/` con `pd.read_csv()`
- Usa `@lru_cache` para cargar cada CSV solo una vez (singleton en memoria)
- `get_stage_times_enriched()` y `get_overall_enriched()` hacen join con entries
- `clear_cache()` limpia la caché (usado en tests)

### `analytics.py`
- `get_stage_result(stage_id)` → tiempos de una etapa ordenados por posición
- `get_overall_at_stage(stage_id)` → clasificación acumulada en una etapa
- `get_final_classification()` → clasificación tras la última etapa
- `get_driver_evolution(entry_id)` → posiciones de un piloto etapa a etapa
- `get_all_drivers_evolution()` → evolución de todos los pilotos (bump chart)
- `get_driver_comparison(a, b)` → tiempos por etapa de dos pilotos

---

## Cómo probar la API manualmente

Con la API arrancada (`uvicorn backend.app.main:app --reload`):

```bash
# Rallies
curl http://localhost:8000/rallies/

# Etapas
curl http://localhost:8000/stages/

# Tiempos de la SS1
curl http://localhost:8000/stages/101/times

# Clasificación final
curl http://localhost:8000/drivers/classification

# Evolución de posiciones
curl http://localhost:8000/drivers/evolution

# Comparativa Ogier (201) vs Evans (202)
curl "http://localhost:8000/drivers/compare?entry_a=201&entry_b=202"
```

O desde Swagger UI: `http://localhost:8000/docs`

---

## Validaciones del Bloque 2

### V1 — 57 tests pasan
```bash
pytest backend/tests/ -v
→ 57 passed (22 anteriores + 35 nuevos)
```

### V2 — API arranca sin errores
```bash
uvicorn backend.app.main:app --reload
→ Uvicorn running on http://0.0.0.0:8000
```

### V3 — Swagger visible
```
http://localhost:8000/docs
→ 8 endpoints documentados en 3 secciones
```

### V4 — /rallies/ devuelve datos
```
http://localhost:8000/rallies/
→ Lista de 3 rallies en JSON
```

### V5 — /stages/101/times devuelve 6 pilotos
```
http://localhost:8000/stages/101/times
→ entries con 6 pilotos, con driver_name y manufacturer
```

### V6 — /drivers/classification devuelve clasificación final
```
http://localhost:8000/drivers/classification
→ 6 pilotos ordenados, líder con diff_first_s=0.0
```

### V7 — /drivers/compare funciona
```
http://localhost:8000/drivers/compare?entry_a=201&entry_b=202
→ Ogier vs Evans con 5 tiempos de etapa cada uno
```

---

## Posibles errores comunes

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: pydantic_settings` | Falta en requirements.txt | `pip install pydantic-settings==2.3.0` |
| `CSV no encontrado` en logs | No se ejecutó el pipeline del Bloque 1 | `WRC_USE_MOCK=true python -m ingestion.pipeline` |
| `422 Unprocessable Entity` | Parámetros de query incorrectos | Revisar los tipos en la URL |
| `404` en `/drivers/compare` | entry_id no existe | Usar IDs válidos: 201-206 |

---

*Siguiente: Bloque 3 — Dashboard Streamlit con gráficos Plotly.*
````

## File: docs/bloque-04-graficos.md
````markdown
# Bloque 4 — Graficos Avanzados y Pulido Visual

## Lecciones del Bloque 3

| Problema | Causa | Solucion |
|---|---|---|
| `utf-8 codec can't decode` en dashboard | Windows guarda archivos como cp1252 | `encoding="utf-8-sig"` al leer/escribir CSVs |
| `ModuleNotFoundError: dashboard` en Streamlit | Streamlit ejecuta desde subcarpeta, root no esta en sys.path | `sys.path.insert(0, ...)` al inicio de cada pagina |
| Archivo `app.py` corrupto | Windows corrompio emojis y caracteres al copiar del zip | Reescribir desde terminal con encoding UTF-8 explicito |

---

## Objetivo

Corregir todos los bugs visuales detectados en el Bloque 3 y pulir la calidad
visual del dashboard para que quede a nivel de portfolio profesional.

---

## Bugs corregidos

### Bug 1: Bump chart y gap chart comprimidos (root cause)

**Problema:** Todos los datos aparecian en una sola columna. El eje X no mostraba
las etapas SS1-SS5.

**Causa raiz:** Los CSVs generados por el pipeline incluyen la columna `stage_code`.
Las funciones de `analytics.py` hacian un merge adicional con la tabla de stages
(que tambien tiene `stage_code`), generando columnas duplicadas `stage_code_x`
y `stage_code_y`. Al intentar acceder a `row["stage_code"]`, Pandas devolvia `""`
porque la columna real era `stage_code_x`.

**Solucion:** Eliminar el merge redundante en `analytics.py`. Si `stage_code` ya
existe en el DataFrame, no volver a hacer merge con stages.

```python
# ANTES (bug)
result = df.merge(stages[["stage_id", "stage_code"]], on="stage_id", how="left")
# → crea stage_code_x y stage_code_y

# DESPUES (fix)
# stage_code ya existe en el CSV, no hace falta merge adicional
result = df.copy()
```

### Bug 2: Tabla comparativa con filas duplicadas

**Problema:** La tabla de comparativa mostraba muchas filas repetidas con los
mismos tiempos para el piloto A.

**Causa:** El merge `df_a.merge(df_b, on="stage_code")` en `03_compare.py`
generaba un producto cartesiano cuando los DataFrames tenian indices no alineados.

**Solucion:** Reescribir la tabla iterando sobre las etapas del piloto A y haciendo
lookup manual del piloto B, garantizando exactamente una fila por etapa.

### Bug 3: Bar chart sin nombres de pilotos visibles

**Problema:** El eje Y del bar chart de etapas no mostraba los nombres.

**Causa:** La columna `y_label` no tenia `automargin=True` en el layout, cortando
los nombres largos.

**Solucion:** Añadir `automargin=True` al eje Y y ajustar `margin=dict(l=10, r=100)`.

### Bug 4: Eje X categorico no respetado

**Problema:** Plotly interpretaba los codigos de etapa (SS1, SS2...) como strings
ordinarios, no como categorias ordenadas.

**Solucion:** Usar `type="category"` y `categoryorder="array"` con el orden
explicito en todos los graficos con eje X de etapas.

---

## Mejoras visuales aplicadas

### Paleta de colores profesional

Sustitucion de rojo/azul puros por colores motorsport mas sobrios:

| Fabricante | Color anterior | Color nuevo |
|---|---|---|
| Toyota | `#EB0A1E` (rojo puro) | `#C8102E` (rojo Toyota oficial) |
| Hyundai | `#003399` (azul puro) | `#003B8E` (azul marino Hyundai) |

### Layout base compartido

Todos los graficos usan `_base_layout()` con configuracion consistente:
- Fondo: `#FAFAFA` (casi blanco, no blanco puro)
- Grid: `#E8E8E8` (gris muy suave)
- Fuente: Inter/Arial, 12px, `#1A1A2E`
- Hover: fondo blanco, borde suave

### Mejoras por grafico

| Grafico | Mejora |
|---|---|
| Bar chart etapas | `automargin=True` en eje Y, nombres completos visibles |
| Bump chart | Eje X categorico ordenado, marcadores con borde blanco |
| Gap chart | Eje Y con `rangemode="tozero"`, etapas ordenadas cronologicamente |
| Comparativa | Tiempos ordenados por `stage_id`, sin duplicados |

---

## Archivos modificados

```
backend/app/services/analytics.py   ← fix: eliminar merge redundante de stage_code
dashboard/components/charts.py      ← reescrito: paleta profesional + axes fixes
dashboard/pages/01_stages.py        ← sys.path fix + mejoras menores
dashboard/pages/02_evolution.py     ← sys.path fix + fix datos bump chart
dashboard/pages/03_compare.py       ← fix tabla duplicada + fix wins calculation
docs/bloque-04-graficos.md          ← este archivo
```

---

## Validaciones del Bloque 4

### V1 — Tests siguen pasando
```bash
pytest backend/tests/ -v
→ 51 passed
```

### V2 — Bump chart muestra todas las etapas
```
Pagina Evolucion → bump chart con SS1-SS5 en eje X
→ Cada piloto tiene una linea continua a traves de las 5 etapas
```

### V3 — Gap chart con ejes correctos
```
Pagina Evolucion → gap chart
→ Eje X: SS1-SS5. Eje Y: segundos. Lineas separadas por piloto
```

### V4 — Bar chart con nombres visibles
```
Pagina Etapas → bar chart
→ Eje Y muestra "Nombre Piloto #XX" para cada barra
```

### V5 — Tabla comparativa sin duplicados
```
Pagina Comparativa → tabla detalle
→ Exactamente 5 filas (una por etapa), sin repeticiones
```

### V6 — Paleta de colores profesional
```
Todos los graficos → colores sobrios, consistentes entre paginas
```

---

## Posibles errores comunes

| Error | Causa | Solucion |
|---|---|---|
| Graficos siguen en blanco | Cache del navegador | Ctrl+Shift+R para hard reload |
| `stage_code` vacio en DataFrame | Pipeline antiguo sin la columna | `rm data/processed/*.csv && WRC_USE_MOCK=true python -m ingestion.pipeline` |
| Bump chart con un solo punto | `stage_code` sigue siendo `stage_code_x` | Verificar que `analytics.py` esta actualizado |

---

*Siguiente: Bloque 5 — Pulido final, README y deploy.*
````

## File: ingestion/__init__.py
````python

````

## File: ingestion/mock_data.py
````python
"""
Datos mock basados en la estructura real de la WRC Live Timing API.

Simulan el Rally Monte Carlo 2024 con 6 pilotos y 5 etapas.
Se usan cuando la API real no está accesible (red corporativa, desarrollo offline).
"""

from __future__ import annotations

# ── Temporada activa ──────────────────────────────────────────────────────────
MOCK_SEASON: dict = {
    "rallyEvents": {
        "items": [
            {
                "id": 1,
                "name": "Rallye Automobile Monte Carlo",
                "status": "Completed",
                "rally": {
                    "country": {"name": "France", "iso2": "FR", "iso3": "FRA"}
                },
                "eventDays": [
                    {"startDate": "2024-01-25T00:00:00"},
                    {"startDate": "2024-01-26T00:00:00"},
                    {"startDate": "2024-01-27T00:00:00"},
                    {"finishDate": "2024-01-28T00:00:00"},
                ],
                "winner": {"driver": {"fullName": "Sébastien Ogier"}},
            },
            {
                "id": 2,
                "name": "Rally Sweden",
                "status": "Completed",
                "rally": {
                    "country": {"name": "Sweden", "iso2": "SE", "iso3": "SWE"}
                },
                "eventDays": [
                    {"startDate": "2024-02-15T00:00:00"},
                    {"finishDate": "2024-02-18T00:00:00"},
                ],
                "winner": {"driver": {"fullName": "Elfyn Evans"}},
            },
            {
                "id": 3,
                "name": "Safari Rally Kenya",
                "status": "Completed",
                "rally": {
                    "country": {"name": "Kenya", "iso2": "KE", "iso3": "KEN"}
                },
                "eventDays": [
                    {"startDate": "2024-03-28T00:00:00"},
                    {"finishDate": "2024-03-31T00:00:00"},
                ],
                "winner": {"driver": {"fullName": "Thierry Neuville"}},
            },
        ]
    }
}

# ── Itinerario (Monte Carlo) ───────────────────────────────────────────────────
MOCK_ITINERARY: dict = {
    "rallyId": 1,
    "itineraryLegs": [
        {
            "itineraryLegId": 10,
            "name": "Leg 1",
            "startListId": 100,
            "itinerarySections": [
                {
                    "itinerarySectionId": 20,
                    "stages": [
                        {
                            "stageId": 101,
                            "code": "SS1",
                            "name": "Col de Turini",
                            "distance": 18.55,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                        {
                            "stageId": 102,
                            "code": "SS2",
                            "name": "La Cabanette - Col de Braus",
                            "distance": 12.3,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                    ],
                }
            ],
        },
        {
            "itineraryLegId": 11,
            "name": "Leg 2",
            "startListId": 101,
            "itinerarySections": [
                {
                    "itinerarySectionId": 21,
                    "stages": [
                        {
                            "stageId": 103,
                            "code": "SS3",
                            "name": "Lucéram - Lantosque",
                            "distance": 22.1,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                        {
                            "stageId": 104,
                            "code": "SS4",
                            "name": "Saint-Léger - Escragnolles",
                            "distance": 15.8,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                    ],
                }
            ],
        },
        {
            "itineraryLegId": 12,
            "name": "Leg 3",
            "startListId": 102,
            "itinerarySections": [
                {
                    "itinerarySectionId": 22,
                    "stages": [
                        {
                            "stageId": 105,
                            "code": "SS5",
                            "name": "Col de Turini (Power Stage)",
                            "distance": 18.55,
                            "stageType": "Tarmac",
                            "status": "Completed",
                        },
                    ],
                }
            ],
        },
    ],
}

# ── Pilotos inscritos ─────────────────────────────────────────────────────────
MOCK_ENTRIES: list[dict] = [
    {
        "entryId": 201,
        "identifier": "17",
        "driver": {"fullName": "Sébastien Ogier", "code": "OGI", "country": {"iso2": "FR"}},
        "codriver": {"fullName": "Vincent Landais"},
        "manufacturer": {"name": "Toyota"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 202,
        "identifier": "33",
        "driver": {"fullName": "Elfyn Evans", "code": "EVA", "country": {"iso2": "GB"}},
        "codriver": {"fullName": "Scott Martin"},
        "manufacturer": {"name": "Toyota"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 203,
        "identifier": "11",
        "driver": {"fullName": "Thierry Neuville", "code": "NEU", "country": {"iso2": "BE"}},
        "codriver": {"fullName": "Martijn Wydaeghe"},
        "manufacturer": {"name": "Hyundai"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 204,
        "identifier": "6",
        "driver": {"fullName": "Ott Tänak", "code": "TAN", "country": {"iso2": "EE"}},
        "codriver": {"fullName": "Martin Järveoja"},
        "manufacturer": {"name": "Hyundai"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 205,
        "identifier": "69",
        "driver": {"fullName": "Kalle Rovanperä", "code": "ROV", "country": {"iso2": "FI"}},
        "codriver": {"fullName": "Jonne Halttunen"},
        "manufacturer": {"name": "Toyota"},
        "group": {"name": "WRC"},
    },
    {
        "entryId": 206,
        "identifier": "8",
        "driver": {"fullName": "Ott Tänak", "code": "TAN", "country": {"iso2": "EE"}},
        "codriver": {"fullName": "Andreas Mikkelsen"},
        "manufacturer": {"name": "Hyundai"},
        "group": {"name": "WRC"},
    },
]

# ── Tiempos por etapa ─────────────────────────────────────────────────────────
# Formato: stage_id → lista de tiempos
# Tiempos en milisegundos, basados en ritmos reales del WRC (~1 min/km en tarmac)

MOCK_STAGE_TIMES: dict[int, list[dict]] = {
    101: [  # SS1 — Col de Turini (18.55 km) → ~14 min
        {"entryId": 201, "position": 1, "elapsedDurationMs": 834_500, "diffFirstMs": 0,     "diffPrevMs": 0,    "status": "Completed"},
        {"entryId": 202, "position": 2, "elapsedDurationMs": 836_200, "diffFirstMs": 1_700, "diffPrevMs": 1_700, "status": "Completed"},
        {"entryId": 203, "position": 3, "elapsedDurationMs": 837_800, "diffFirstMs": 3_300, "diffPrevMs": 1_600, "status": "Completed"},
        {"entryId": 205, "position": 4, "elapsedDurationMs": 839_100, "diffFirstMs": 4_600, "diffPrevMs": 1_300, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 841_000, "diffFirstMs": 6_500, "diffPrevMs": 1_900, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 844_300, "diffFirstMs": 9_800, "diffPrevMs": 3_300, "status": "Completed"},
    ],
    102: [  # SS2 — La Cabanette (12.3 km) → ~9.5 min
        {"entryId": 203, "position": 1, "elapsedDurationMs": 572_000, "diffFirstMs": 0,     "diffPrevMs": 0,    "status": "Completed"},
        {"entryId": 201, "position": 2, "elapsedDurationMs": 573_500, "diffFirstMs": 1_500, "diffPrevMs": 1_500, "status": "Completed"},
        {"entryId": 205, "position": 3, "elapsedDurationMs": 575_200, "diffFirstMs": 3_200, "diffPrevMs": 1_700, "status": "Completed"},
        {"entryId": 202, "position": 4, "elapsedDurationMs": 577_400, "diffFirstMs": 5_400, "diffPrevMs": 2_200, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 579_800, "diffFirstMs": 7_800, "diffPrevMs": 2_400, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 583_100, "diffFirstMs": 11_100,"diffPrevMs": 3_300, "status": "Completed"},
    ],
    103: [  # SS3 — Lucéram (22.1 km) → ~17 min
        {"entryId": 201, "position": 1, "elapsedDurationMs": 1_018_000, "diffFirstMs": 0,      "diffPrevMs": 0,     "status": "Completed"},
        {"entryId": 203, "position": 2, "elapsedDurationMs": 1_020_500, "diffFirstMs": 2_500,  "diffPrevMs": 2_500, "status": "Completed"},
        {"entryId": 202, "position": 3, "elapsedDurationMs": 1_022_100, "diffFirstMs": 4_100,  "diffPrevMs": 1_600, "status": "Completed"},
        {"entryId": 205, "position": 4, "elapsedDurationMs": 1_025_300, "diffFirstMs": 7_300,  "diffPrevMs": 3_200, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 1_028_700, "diffFirstMs": 10_700, "diffPrevMs": 3_400, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 1_034_200, "diffFirstMs": 16_200, "diffPrevMs": 5_500, "status": "Completed"},
    ],
    104: [  # SS4 — Saint-Léger (15.8 km) → ~12 min
        {"entryId": 202, "position": 1, "elapsedDurationMs": 731_200, "diffFirstMs": 0,      "diffPrevMs": 0,     "status": "Completed"},
        {"entryId": 201, "position": 2, "elapsedDurationMs": 732_800, "diffFirstMs": 1_600,  "diffPrevMs": 1_600, "status": "Completed"},
        {"entryId": 205, "position": 3, "elapsedDurationMs": 734_500, "diffFirstMs": 3_300,  "diffPrevMs": 1_700, "status": "Completed"},
        {"entryId": 203, "position": 4, "elapsedDurationMs": 736_000, "diffFirstMs": 4_800,  "diffPrevMs": 1_500, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 739_400, "diffFirstMs": 8_200,  "diffPrevMs": 3_400, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 743_100, "diffFirstMs": 11_900, "diffPrevMs": 3_700, "status": "Completed"},
    ],
    105: [  # SS5 — Power Stage (18.55 km) → ~14 min
        {"entryId": 205, "position": 1, "elapsedDurationMs": 828_300, "diffFirstMs": 0,     "diffPrevMs": 0,    "status": "Completed"},
        {"entryId": 201, "position": 2, "elapsedDurationMs": 829_700, "diffFirstMs": 1_400, "diffPrevMs": 1_400, "status": "Completed"},
        {"entryId": 203, "position": 3, "elapsedDurationMs": 831_200, "diffFirstMs": 2_900, "diffPrevMs": 1_500, "status": "Completed"},
        {"entryId": 202, "position": 4, "elapsedDurationMs": 833_800, "diffFirstMs": 5_500, "diffPrevMs": 2_600, "status": "Completed"},
        {"entryId": 204, "position": 5, "elapsedDurationMs": 836_500, "diffFirstMs": 8_200, "diffPrevMs": 2_700, "status": "Completed"},
        {"entryId": 206, "position": 6, "elapsedDurationMs": 841_000, "diffFirstMs": 12_700,"diffPrevMs": 4_500, "status": "Completed"},
    ],
}

# ── Clasificación general acumulada ───────────────────────────────────────────
# Calculada acumulando los tiempos de etapa

MOCK_OVERALL: dict[int, list[dict]] = {
    101: [  # Tras SS1
        {"entryId": 201, "position": 1, "totalTimeMs": 834_500,   "diffFirstMs": 0,     "penaltyTimeMs": 0},
        {"entryId": 202, "position": 2, "totalTimeMs": 836_200,   "diffFirstMs": 1_700, "penaltyTimeMs": 0},
        {"entryId": 203, "position": 3, "totalTimeMs": 837_800,   "diffFirstMs": 3_300, "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 839_100,   "diffFirstMs": 4_600, "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 841_000,   "diffFirstMs": 6_500, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 844_300,   "diffFirstMs": 9_800, "penaltyTimeMs": 0},
    ],
    102: [  # Tras SS2
        {"entryId": 201, "position": 1, "totalTimeMs": 1_408_000, "diffFirstMs": 0,      "penaltyTimeMs": 0},
        {"entryId": 203, "position": 2, "totalTimeMs": 1_409_800, "diffFirstMs": 1_800,  "penaltyTimeMs": 0},
        {"entryId": 202, "position": 3, "totalTimeMs": 1_413_600, "diffFirstMs": 5_600,  "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 1_414_300, "diffFirstMs": 6_300,  "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 1_420_800, "diffFirstMs": 12_800, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 1_427_400, "diffFirstMs": 19_400, "penaltyTimeMs": 0},
    ],
    103: [  # Tras SS3
        {"entryId": 201, "position": 1, "totalTimeMs": 2_426_000, "diffFirstMs": 0,      "penaltyTimeMs": 0},
        {"entryId": 203, "position": 2, "totalTimeMs": 2_430_300, "diffFirstMs": 4_300,  "penaltyTimeMs": 0},
        {"entryId": 202, "position": 3, "totalTimeMs": 2_435_700, "diffFirstMs": 9_700,  "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 2_439_600, "diffFirstMs": 13_600, "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 2_449_500, "diffFirstMs": 23_500, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 2_461_600, "diffFirstMs": 35_600, "penaltyTimeMs": 0},
    ],
    104: [  # Tras SS4
        {"entryId": 201, "position": 1, "totalTimeMs": 3_158_800, "diffFirstMs": 0,      "penaltyTimeMs": 0},
        {"entryId": 203, "position": 2, "totalTimeMs": 3_166_300, "diffFirstMs": 7_500,  "penaltyTimeMs": 0},
        {"entryId": 202, "position": 3, "totalTimeMs": 3_166_900, "diffFirstMs": 8_100,  "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 3_174_100, "diffFirstMs": 15_300, "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 3_188_900, "diffFirstMs": 30_100, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 3_204_700, "diffFirstMs": 45_900, "penaltyTimeMs": 0},
    ],
    105: [  # Tras SS5 — Clasificación final
        {"entryId": 201, "position": 1, "totalTimeMs": 3_988_500, "diffFirstMs": 0,      "penaltyTimeMs": 0},
        {"entryId": 203, "position": 2, "totalTimeMs": 3_997_500, "diffFirstMs": 9_000,  "penaltyTimeMs": 0},
        {"entryId": 202, "position": 3, "totalTimeMs": 4_000_700, "diffFirstMs": 12_200, "penaltyTimeMs": 0},
        {"entryId": 205, "position": 4, "totalTimeMs": 4_002_400, "diffFirstMs": 13_900, "penaltyTimeMs": 0},
        {"entryId": 204, "position": 5, "totalTimeMs": 4_025_400, "diffFirstMs": 36_900, "penaltyTimeMs": 0},
        {"entryId": 206, "position": 6, "totalTimeMs": 4_045_700, "diffFirstMs": 57_200, "penaltyTimeMs": 0},
    ],
}
````

## File: ingestion/transformers.py
````python
"""
Transformadores de datos WRC.

Reciben dicts/listas crudos de la API y devuelven
DataFrames de Pandas limpios y normalizados.
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _ms_to_seconds(ms: int | None) -> float | None:
    """Convierte milisegundos a segundos con 3 decimales."""
    if ms is None:
        return None
    return round(ms / 1000, 3)


def _ms_to_timestr(ms: int | None) -> str | None:
    """Convierte milisegundos a string legible HH:MM:SS.mmm"""
    if ms is None:
        return None
    total_s = ms / 1000
    hours = int(total_s // 3600)
    minutes = int((total_s % 3600) // 60)
    seconds = total_s % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"


# ── Eventos ──────────────────────────────────────────────────────────────────

def transform_events(raw_events: list[dict]) -> pd.DataFrame:
    """
    Normaliza la lista de eventos de la temporada.

    Columnas: event_id, name, status, country, date_start, date_finish.
    """
    rows = []
    for ev in raw_events:
        rally = ev.get("rally", {})
        days = ev.get("eventDays", [])
        date_start = days[0].get("startDate", "") if days else ""
        date_finish = days[-1].get("finishDate", "") if days else ""

        rows.append({
            "event_id": ev.get("id"),
            "name": ev.get("name", ""),
            "status": ev.get("status", ""),
            "country": rally.get("country", {}).get("name", ""),
            "country_iso": rally.get("country", {}).get("iso2", ""),
            "date_start": date_start,
            "date_finish": date_finish,
        })

    df = pd.DataFrame(rows)
    logger.info("Eventos transformados: %d filas", len(df))
    return df


# ── Etapas ───────────────────────────────────────────────────────────────────

def transform_stages(itinerary: dict) -> pd.DataFrame:
    """
    Extrae y aplana todas las etapas del itinerario.

    Columnas: stage_id, stage_code, name, distance_km, surface, leg_name, day.
    """
    rows = []
    legs = itinerary.get("itineraryLegs", [])

    for leg in legs:
        leg_name = leg.get("name", "")
        day = leg.get("startListId", "")
        sections = leg.get("itinerarySections", [])

        for section in sections:
            stages = section.get("stages", [])
            for stage in stages:
                rows.append({
                    "stage_id": stage.get("stageId"),
                    "stage_code": stage.get("code", ""),
                    "name": stage.get("name", ""),
                    "distance_km": stage.get("distance", 0.0),
                    "surface": stage.get("stageType", ""),
                    "leg_name": leg_name,
                    "status": stage.get("status", ""),
                })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna(subset=["stage_id"])
        df["stage_id"] = df["stage_id"].astype(int)
    logger.info("Etapas transformadas: %d filas", len(df))
    return df


# ── Pilotos (entries) ────────────────────────────────────────────────────────

def transform_entries(raw_entries: list[dict]) -> pd.DataFrame:
    """
    Normaliza la lista de pilotos inscritos.

    Columnas: entry_id, driver_name, codriver_name, manufacturer,
              car_number, group, nationality.
    """
    rows = []
    for entry in raw_entries:
        driver = entry.get("driver", {})
        codriver = entry.get("codriver", {})
        rows.append({
            "entry_id": entry.get("entryId"),
            "driver_name": driver.get("fullName", ""),
            "driver_code": driver.get("code", ""),
            "driver_nationality": driver.get("country", {}).get("iso2", ""),
            "codriver_name": codriver.get("fullName", ""),
            "manufacturer": entry.get("manufacturer", {}).get("name", ""),
            "car_number": entry.get("identifier", ""),
            "group": entry.get("group", {}).get("name", ""),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna(subset=["entry_id"])
        df["entry_id"] = df["entry_id"].astype(int)
    logger.info("Pilotos transformados: %d filas", len(df))
    return df


# ── Tiempos de etapa ─────────────────────────────────────────────────────────

def transform_stage_times(
    raw_times: list[dict],
    stage_id: int,
    event_id: int,
) -> pd.DataFrame:
    """
    Normaliza los tiempos de una etapa concreta.

    Columnas: event_id, stage_id, entry_id, position,
              time_ms, time_s, time_str, diff_first_ms, diff_first_s, status.
    """
    rows = []
    for t in raw_times:
        rows.append({
            "event_id": event_id,
            "stage_id": stage_id,
            "entry_id": t.get("entryId"),
            "position": t.get("position"),
            "time_ms": t.get("elapsedDurationMs"),
            "time_s": _ms_to_seconds(t.get("elapsedDurationMs")),
            "time_str": _ms_to_timestr(t.get("elapsedDurationMs")),
            "diff_first_ms": t.get("diffFirstMs"),
            "diff_first_s": _ms_to_seconds(t.get("diffFirstMs")),
            "diff_prev_ms": t.get("diffPrevMs"),
            "diff_prev_s": _ms_to_seconds(t.get("diffPrevMs")),
            "status": t.get("status", ""),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna(subset=["entry_id"])
        df["entry_id"] = df["entry_id"].astype(int)
        df = df.sort_values("position").reset_index(drop=True)
    logger.info(
        "Stage times transformados: event=%d stage=%d → %d filas",
        event_id, stage_id, len(df)
    )
    return df


# ── Clasificación general ────────────────────────────────────────────────────

def transform_overall_results(
    raw_results: list[dict],
    stage_id: int,
    event_id: int,
) -> pd.DataFrame:
    """
    Normaliza la clasificación general acumulada tras una etapa.

    Columnas: event_id, stage_id, entry_id, position,
              total_time_ms, total_time_s, total_time_str,
              diff_first_ms, diff_first_s.
    """
    rows = []
    for r in raw_results:
        rows.append({
            "event_id": event_id,
            "stage_id": stage_id,
            "entry_id": r.get("entryId"),
            "position": r.get("position"),
            "total_time_ms": r.get("totalTimeMs"),
            "total_time_s": _ms_to_seconds(r.get("totalTimeMs")),
            "total_time_str": _ms_to_timestr(r.get("totalTimeMs")),
            "diff_first_ms": r.get("diffFirstMs"),
            "diff_first_s": _ms_to_seconds(r.get("diffFirstMs")),
            "status": r.get("penaltyTimeMs", "OK"),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna(subset=["entry_id"])
        df["entry_id"] = df["entry_id"].astype(int)
        df = df.sort_values("position").reset_index(drop=True)
    logger.info(
        "Overall results transformados: event=%d stage=%d → %d filas",
        event_id, stage_id, len(df)
    )
    return df
````

## File: ingestion/wrc_client.py
````python
"""
Cliente HTTP para la WRC Live Timing API.

Soporta dos modos controlados por la variable de entorno WRC_USE_MOCK:
  - WRC_USE_MOCK=false (default)  → llamadas reales a api.wrc.com
  - WRC_USE_MOCK=true             → datos mock locales (desarrollo offline)
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from ingestion import mock_data as mock

logger = logging.getLogger(__name__)

# ── Configuración ─────────────────────────────────────────────────────────────
_SEASON_URL = "https://api.wrc.com/contel-page/83388/calendar/active-season/"
_RESULTS_BASE = "https://api.wrc.com/results-api"
_TIMEOUT = 15.0


def _use_mock() -> bool:
    """Devuelve True si WRC_USE_MOCK=true en el entorno o .env."""
    return os.getenv("WRC_USE_MOCK", "false").lower() == "true"


def _get(url: str, params: dict[str, Any] | None = None) -> Any:
    """Realiza una petición GET y devuelve el JSON parseado."""
    try:
        response = httpx.get(url, params=params, timeout=_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error %s al llamar %s", e.response.status_code, url)
        raise
    except httpx.RequestError as e:
        logger.error("Error de conexión al llamar %s: %s", url, e)
        raise


# ── Endpoints ─────────────────────────────────────────────────────────────────

def get_active_season() -> list[dict]:
    """Devuelve la lista de eventos de la temporada activa."""
    if _use_mock():
        logger.info("[MOCK] Cargando temporada activa desde mock_data")
        items = mock.MOCK_SEASON["rallyEvents"]["items"]
        logger.info("Temporada activa (mock): %d eventos", len(items))
        return items

    data = _get(_SEASON_URL)
    items = data.get("rallyEvents", {}).get("items", [])
    logger.info("Temporada activa: %d eventos encontrados", len(items))
    return items


def get_itinerary(event_id: int) -> dict:
    """Devuelve el itinerario completo de un evento."""
    if _use_mock():
        logger.info("[MOCK] Cargando itinerario para event_id=%d", event_id)
        return mock.MOCK_ITINERARY

    url = f"{_RESULTS_BASE}/rally-event/{event_id}/itinerary"
    return _get(url)


def get_entries(event_id: int) -> list[dict]:
    """Devuelve la lista de pilotos inscritos en un evento."""
    if _use_mock():
        logger.info("[MOCK] Cargando pilotos para event_id=%d", event_id)
        return mock.MOCK_ENTRIES

    url = f"{_RESULTS_BASE}/rally-event/{event_id}/cars"
    return _get(url)


def get_stage_times(event_id: int, stage_id: int) -> list[dict]:
    """Devuelve los tiempos de todos los pilotos en una etapa concreta."""
    if _use_mock():
        logger.info("[MOCK] Cargando stage_times para stage_id=%d", stage_id)
        return mock.MOCK_STAGE_TIMES.get(stage_id, [])

    url = (
        f"{_RESULTS_BASE}/rally-event/{event_id}"
        f"/stage-times/stage-external/{stage_id}"
    )
    return _get(url)


def get_overall_results(event_id: int, stage_id: int) -> list[dict]:
    """Devuelve la clasificación general acumulada hasta una etapa dada."""
    if _use_mock():
        logger.info("[MOCK] Cargando overall para stage_id=%d", stage_id)
        return mock.MOCK_OVERALL.get(stage_id, [])

    url = f"{_RESULTS_BASE}/rally-event/{event_id}/results/{stage_id}/stage-overall"
    return _get(url)


def get_split_times(event_id: int, stage_id: int) -> dict:
    """Devuelve los split times de una etapa."""
    if _use_mock():
        logger.info("[MOCK] Split times no disponibles en mock, devolviendo vacío")
        return {}

    url = (
        f"{_RESULTS_BASE}/rally-event/{event_id}"
        f"/stage-times/stage-external/{stage_id}/split-times"
    )
    return _get(url)
````

## File: Makefile
````makefile
.PHONY: install run-api run-dashboard test help

# ── Setup ──────────────────────────────────────────────────────────
install:
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	cp -n .env.example .env || true
	@echo "✅  Entorno listo. Activa con: source venv/bin/activate"

# ── Run ────────────────────────────────────────────────────────────
run-api:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard:
	streamlit run dashboard/app.py --server.port 8501

# ── Tests ──────────────────────────────────────────────────────────
test:
	pytest backend/tests/ -v

# ── Help ───────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make install        Crea venv e instala dependencias"
	@echo "  make run-api        Arranca FastAPI en localhost:8000"
	@echo "  make run-dashboard  Arranca Streamlit en localhost:8501"
	@echo "  make test           Ejecuta los tests"
	@echo ""
````

## File: pytest.ini
````ini
[pytest]
testpaths = backend/tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
````

## File: requirements.txt
````
# ── Web framework ─────────────────────────────────────────────────
fastapi==0.111.0
uvicorn[standard]==0.29.0

# ── Dashboard ─────────────────────────────────────────────────────
streamlit==1.35.0

# ── Data processing ───────────────────────────────────────────────
pandas==2.2.2
numpy==1.26.4

# ── Visualisation ─────────────────────────────────────────────────
plotly==5.22.0

# ── HTTP client (WRC API ingestion) ───────────────────────────────
httpx==0.27.0

# ── Validation ────────────────────────────────────────────────────
pydantic==2.7.1
pydantic-settings==2.3.0

# ── Testing ───────────────────────────────────────────────────────
pytest==8.2.0
pytest-asyncio==0.23.6
httpx==0.27.0          # also used as AsyncClient in tests

# ── Utilities ─────────────────────────────────────────────────────
python-dotenv==1.0.1
````

## File: backend/app/services/analytics.py
````python
"""
Servicio de analitica.

Funciones de calculo y transformacion sobre los DataFrames cargados.
"""

from __future__ import annotations

import logging

import pandas as pd

from backend.app.services import data_loader as loader

logger = logging.getLogger(__name__)


def get_stage_result(stage_id: int) -> pd.DataFrame:
    """Tiempos enriquecidos de una etapa concreta, ordenados por posicion."""
    df = loader.get_stage_times_enriched()
    if df.empty:
        return df
    result = df[df["stage_id"] == stage_id].sort_values("position")
    return result.reset_index(drop=True)


def get_overall_at_stage(stage_id: int) -> pd.DataFrame:
    """Clasificacion general enriquecida tras una etapa concreta."""
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    result = df[df["stage_id"] == stage_id].sort_values("position")
    return result.reset_index(drop=True)


def get_final_classification() -> pd.DataFrame:
    """Clasificacion final del rally (tras la ultima etapa)."""
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    last_stage = df["stage_id"].max()
    return get_overall_at_stage(last_stage)


def get_driver_evolution(entry_id: int) -> pd.DataFrame:
    """Evolucion de posicion de un piloto etapa a etapa."""
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    # stage_code ya existe en el CSV — no hace falta merge adicional
    result = df[df["entry_id"] == entry_id].copy()
    return result.sort_values("stage_id").reset_index(drop=True)


def get_all_drivers_evolution() -> pd.DataFrame:
    """Evolucion de posicion de todos los pilotos (bump chart)."""
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    # stage_code ya existe en el CSV — no hace falta merge adicional
    # Solo aseguramos que la columna existe; si no, usamos stage_id como fallback
    if "stage_code" not in df.columns:
        stages = loader.get_stages()[["stage_id", "stage_code"]].copy()
        df = df.merge(stages, on="stage_id", how="left")
    return df.sort_values(["entry_id", "stage_id"]).reset_index(drop=True)


def get_driver_comparison(entry_id_a: int, entry_id_b: int) -> dict:
    """Tiempos por etapa de dos pilotos para comparativa."""
    times = loader.get_stage_times_enriched()

    def _get_driver_times(entry_id: int) -> pd.DataFrame:
        df = times[times["entry_id"] == entry_id].copy()
        # stage_code ya existe en el CSV — no hace falta merge adicional
        if "stage_code" not in df.columns:
            stages = loader.get_stages()[["stage_id", "stage_code"]]
            df = df.merge(stages, on="stage_id", how="left")
        return df.sort_values("stage_id").reset_index(drop=True)

    return {
        "driver_a": _get_driver_times(entry_id_a),
        "driver_b": _get_driver_times(entry_id_b),
    }
````

## File: backend/app/services/data_loader.py
````python
"""
Servicio de carga de datos.

Carga los CSVs procesados como DataFrames de Pandas y los cachea en memoria.
Se inicializa una sola vez al arrancar la API.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_PROCESSED_DIR = _PROJECT_ROOT / "data" / "processed"

# Prefijo del evento principal (Monte Carlo)
_EVENT_PREFIX = "rallye_automobile_monte_carlo"


def _load_csv(filename: str) -> pd.DataFrame:
    """Carga un CSV desde data/processed/ con manejo de errores."""
    path = _PROCESSED_DIR / filename
    if not path.exists():
        logger.warning("CSV no encontrado: %s — devolviendo DataFrame vacío", filename)
        return pd.DataFrame()
    df = pd.read_csv(path)
    logger.info("CSV cargado: %s (%d filas)", filename, len(df))
    return df


# ── Carga de datos ────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def get_events() -> pd.DataFrame:
    """Devuelve los eventos de la temporada."""
    return _load_csv("events.csv")


@lru_cache(maxsize=1)
def get_stages() -> pd.DataFrame:
    """Devuelve las etapas del rally principal."""
    return _load_csv(f"{_EVENT_PREFIX}_stages.csv")


@lru_cache(maxsize=1)
def get_entries() -> pd.DataFrame:
    """Devuelve los pilotos inscritos."""
    return _load_csv(f"{_EVENT_PREFIX}_entries.csv")


@lru_cache(maxsize=1)
def get_stage_times() -> pd.DataFrame:
    """Devuelve todos los tiempos de etapa."""
    return _load_csv(f"{_EVENT_PREFIX}_stage_times.csv")


@lru_cache(maxsize=1)
def get_overall() -> pd.DataFrame:
    """Devuelve la clasificación general acumulada."""
    return _load_csv(f"{_EVENT_PREFIX}_overall.csv")


def get_stage_times_enriched() -> pd.DataFrame:
    """
    Devuelve tiempos de etapa enriquecidos con datos del piloto.

    Join entre stage_times y entries por entry_id.
    """
    times = get_stage_times().copy()
    entries = get_entries()[
        ["entry_id", "driver_name", "driver_code", "manufacturer", "car_number"]
    ]
    if times.empty or entries.empty:
        return times
    return times.merge(entries, on="entry_id", how="left")


def get_overall_enriched() -> pd.DataFrame:
    """
    Devuelve clasificación general enriquecida con datos del piloto.
    """
    overall = get_overall().copy()
    entries = get_entries()[
        ["entry_id", "driver_name", "driver_code", "manufacturer", "car_number"]
    ]
    if overall.empty or entries.empty:
        return overall
    return overall.merge(entries, on="entry_id", how="left")


def clear_cache() -> None:
    """Limpia la caché (útil para tests o recarga de datos)."""
    get_events.cache_clear()
    get_stages.cache_clear()
    get_entries.cache_clear()
    get_stage_times.cache_clear()
    get_overall.cache_clear()
    logger.info("Caché de datos limpiada")
````

## File: dashboard/app.py
````python
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import streamlit as st
from dashboard.components import api_client as api

st.set_page_config(page_title="Rally Performance Analyzer", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.markdown("## Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="Overview")
    st.page_link("pages/01_stages.py", label="Etapas")
    st.page_link("pages/02_evolution.py", label="Evolucion")
    st.page_link("pages/03_compare.py", label="Comparativa")
    st.markdown("---")
    st.caption("Datos: Rally Monte Carlo 2024")

st.title("Rally Performance Analyzer")
st.markdown("**World Rally Championship - Analisis de datos**")
st.divider()

rallies = api.get_rallies()
classification = api.get_classification()
stages = api.get_stages()
drivers = api.get_drivers()

if not rallies or not classification:
    st.error("No se puede conectar con la API. Arranca FastAPI primero.")
    st.code("uvicorn backend.app.main:app --reload")
    st.stop()

rally = rallies[0]
entries = classification.get("entries", [])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Rally", rally["name"].replace("Rallye Automobile ", ""))
with col2:
    st.metric("Pais", rally["country"])
with col3:
    st.metric("Etapas", len(stages))
with col4:
    st.metric("Pilotos", len(drivers))

st.divider()
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### Clasificacion General Final")
    if entries:
        rows = []
        for e in entries:
            gap = e.get("diff_first_s", 0) or 0
            gap_str = "LIDER" if gap == 0 else f"+{gap:.1f}s"
            rows.append({"Pos.": e["position"], "Piloto": e["driver_name"], "#": e.get("car_number", ""), "Fabricante": e.get("manufacturer", ""), "Tiempo total": e.get("total_time_str", "-"), "Gap": gap_str})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

with col_right:
    st.markdown("### Fabricantes")
    fab_data = {}
    for e in entries:
        fab = e.get("manufacturer", "Otro")
        fab_data[fab] = fab_data.get(fab, 0) + 1
    for fab, count in sorted(fab_data.items()):
        st.markdown(f"**{fab}** - {count} pilotos")
    st.markdown("---")
    st.markdown("### Podio")
    medals = ["1.", "2.", "3."]
    for e in entries[:3]:
        gap = e.get("diff_first_s", 0) or 0
        gap_str = "LIDER" if gap == 0 else f"+{gap:.1f}s"
        st.markdown(f"{medals[e['position']-1]} **{e['driver_name']}** ({e.get('manufacturer','')}) - {gap_str}")
````

## File: dashboard/components/charts.py
````python
"""
Graficos Plotly reutilizables para el dashboard.

Paleta profesional motorsport. Todas las funciones reciben un DataFrame
y devuelven un go.Figure listo para st.plotly_chart().
"""

from __future__ import annotations

import plotly.graph_objects as go
import pandas as pd

# ── Paleta coordinada con tema oscuro (config.toml base=dark) ─────────────────
# 20 colores visualmente distintos entre si, legibles sobre fondo oscuro.
# Se asignan por posicion de iteracion (no por fabricante) para que cada
# piloto tenga siempre un color unico aunque comparta equipo.
DRIVER_COLORS = [
    "#FF4B4B",  # rojo vivo
    "#4CC9F0",  # azul electrico
    "#F8961E",  # naranja
    "#7BF1A8",  # verde menta
    "#BB8FCE",  # lavanda
    "#FEE440",  # amarillo
    "#00F5D4",  # cyan
    "#9B5DE5",  # violeta
    "#F72585",  # rosa fuerte
    "#4361EE",  # azul indigo
    "#FB5607",  # naranja rojizo
    "#FFBE0B",  # ambar
    "#06D6A0",  # esmeralda
    "#EF233C",  # rojo carmesi
    "#8338EC",  # purpura
    "#3BF4FB",  # turquesa
    "#E9FF70",  # lima
    "#FF9F1C",  # mandarina
    "#2EC4B6",  # teal
    "#FF6FA8",  # rosa salmon
]

# Solo para la comparativa de dos pilotos donde el equipo aporta contexto visual
MANUFACTURER_COLORS: dict[str, str] = {
    "Toyota":  "#FF4B4B",
    "Hyundai": "#4CC9F0",
    "Ford":    "#F8961E",
    "Citroen": "#7BF1A8",
}

GRID_COLOR  = "#2D2D4E"
BG_COLOR    = "rgba(0,0,0,0)"   # transparente — hereda el fondo oscuro de Streamlit
FONT_COLOR  = "#FFFFFF"
FONT_FAMILY = "Inter, Arial, sans-serif"


def _driver_color(idx: int) -> str:
    return DRIVER_COLORS[idx % len(DRIVER_COLORS)]


def _manufacturer_color(manufacturer: str, idx: int = 0) -> str:
    return MANUFACTURER_COLORS.get(manufacturer, DRIVER_COLORS[idx % len(DRIVER_COLORS)])


def _base_layout(**kwargs) -> dict:
    """Layout base compartido por todos los graficos."""
    _axis = dict(
        gridcolor=GRID_COLOR,
        linecolor="#404060",
        tickfont=dict(color=FONT_COLOR),
        title_font=dict(color=FONT_COLOR),
    )
    base = dict(
        plot_bgcolor=BG_COLOR,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, size=12, color=FONT_COLOR),
        xaxis=_axis,
        yaxis=_axis,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=11, color=FONT_COLOR),
        ),
        margin=dict(l=10, r=90, t=55, b=45),
        hoverlabel=dict(bgcolor="#1A1A2E", font_size=12, font_color=FONT_COLOR),
    )
    base.update(kwargs)
    return base


# ── Grafico 1: Tiempos de etapa (bar horizontal) ──────────────────────────────

def create_stage_times_chart(df: pd.DataFrame, stage_code: str) -> go.Figure:
    """
    Bar chart horizontal de tiempos por etapa.
    Eje Y: nombre del piloto + fabricante. Eje X: tiempo en segundos.
    """
    if df.empty:
        return go.Figure()

    df = df.sort_values("position", ascending=False).copy()

    df["y_label"] = df.apply(
        lambda r: f"{r.get('driver_name','?')}  #{r.get('car_number','')}", axis=1
    )
    df["gap_label"] = df["diff_first_s"].apply(
        lambda x: "LIDER" if (x == 0 or pd.isna(x)) else f"+{x:.3f}s"
    )

    # Color unico por piloto segun su posicion en el ranking
    colors = [_driver_color(i) for i in range(len(df))]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["time_s"],
        y=df["y_label"],
        orientation="h",
        marker=dict(color=colors, opacity=0.85),
        text=df["gap_label"],
        textposition="outside",
        textfont=dict(size=11, color=FONT_COLOR),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Tiempo: %{x:.3f}s<br>"
            "Gap lider: %{text}<extra></extra>"
        ),
    ))

    x_min = df["time_s"].min()
    x_max = df["time_s"].max()
    margin = (x_max - x_min) * 0.15

    layout = _base_layout(
        title=dict(text=f"Tiempos de etapa — {stage_code}", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(
            title="Tiempo (s)",
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
            range=[x_min * 0.998, x_max + margin],
        ),
        yaxis=dict(
            title="",
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            automargin=True,
        ),
        height=350,
        margin=dict(l=10, r=100, t=50, b=45),
    )
    fig.update_layout(**layout)
    return fig


# ── Grafico 2: Gap acumulado respecto al lider ────────────────────────────────

def create_gap_evolution_chart(df: pd.DataFrame) -> go.Figure:
    """
    Line chart del gap acumulado respecto al lider etapa a etapa.
    Eje X: etapas. Eje Y: segundos de diferencia.
    """
    if df.empty:
        return go.Figure()

    stage_order = df.drop_duplicates("stage_id").sort_values("stage_id")["stage_code"].tolist()

    fig = go.Figure()
    drivers = df.drop_duplicates("entry_id").sort_values("entry_id")

    for idx, (_, row) in enumerate(drivers.iterrows()):
        entry_id = row["entry_id"]
        code = row.get("driver_code", str(entry_id))
        color = _driver_color(idx)

        d = df[df["entry_id"] == entry_id].copy()
        d["stage_code"] = pd.Categorical(d["stage_code"], categories=stage_order, ordered=True)
        d = d.sort_values("stage_code")

        fig.add_trace(go.Scatter(
            x=d["stage_code"].astype(str),
            y=d["diff_first_s"].fillna(0),
            mode="lines+markers",
            name=code,
            line=dict(color=color, width=2.5),
            marker=dict(size=8, color=color, line=dict(width=1.5, color="white")),
            hovertemplate=(
                f"<b>{code}</b><br>"
                "Etapa: %{x}<br>"
                "Gap lider: +%{y:.1f}s<extra></extra>"
            ),
        ))

    layout = _base_layout(
        title=dict(text="Gap acumulado respecto al lider", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=stage_order,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=12, color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        yaxis=dict(
            title="Diferencia (s)",
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
            rangemode="tozero",
        ),
        height=400,
    )
    fig.update_layout(**layout)
    return fig


# ── Grafico 3: Evolucion de posiciones (bump chart) ───────────────────────────

def create_position_evolution_chart(df: pd.DataFrame) -> go.Figure:
    """
    Bump chart: posicion de cada piloto en cada etapa.
    Eje Y invertido (posicion 1 arriba). Eje X: etapas categoricas.
    """
    if df.empty:
        return go.Figure()

    stage_order = df.drop_duplicates("stage_id").sort_values("stage_id")["stage_code"].tolist()
    n_drivers = df["entry_id"].nunique()

    fig = go.Figure()
    drivers = df.drop_duplicates("entry_id").sort_values("entry_id")

    for idx, (_, row) in enumerate(drivers.iterrows()):
        entry_id = row["entry_id"]
        code = row.get("driver_code", str(entry_id))
        name = row.get("driver_name", code)
        color = _driver_color(idx)

        d = df[df["entry_id"] == entry_id].copy()
        d["stage_code"] = pd.Categorical(d["stage_code"], categories=stage_order, ordered=True)
        d = d.sort_values("stage_code")

        fig.add_trace(go.Scatter(
            x=d["stage_code"].astype(str),
            y=d["position"],
            mode="lines+markers",
            name=code,
            line=dict(color=color, width=3),
            marker=dict(
                size=12, color=color,
                line=dict(width=2, color="white"),
                symbol="circle",
            ),
            hovertemplate=(
                f"<b>{name}</b><br>"
                "Etapa: %{x}<br>"
                "Posicion: %{y}<extra></extra>"
            ),
        ))

    layout = _base_layout(
        title=dict(text="Evolucion de posiciones por etapa", font=dict(size=15, color=FONT_COLOR)),
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=stage_order,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=13, color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        yaxis=dict(
            title="Posicion",
            autorange="reversed",
            tickmode="linear",
            tick0=1,
            dtick=1,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=12, color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
            range=[n_drivers + 0.5, 0.5],
        ),
        height=440,
        margin=dict(l=10, r=10, t=55, b=45),
    )
    fig.update_layout(**layout)
    return fig


# ── Grafico 4: Comparativa entre dos pilotos ─────────────────────────────────

def create_comparison_chart(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    name_a: str,
    name_b: str,
    manufacturer_a: str = "",
    manufacturer_b: str = "",
) -> go.Figure:
    """
    Grouped bar chart: tiempos de etapa de dos pilotos lado a lado.
    Aqui si se usan colores de fabricante porque el contexto visual aporta informacion.
    """
    if df_a.empty or df_b.empty:
        return go.Figure()

    color_a = _manufacturer_color(manufacturer_a, 0)
    color_b = _manufacturer_color(manufacturer_b, 1)

    stage_order = df_a.sort_values("stage_id")["stage_code"].tolist() if "stage_id" in df_a.columns \
        else df_a["stage_code"].tolist()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=name_a,
        x=df_a.sort_values("stage_id")["stage_code"] if "stage_id" in df_a.columns else df_a["stage_code"],
        y=df_a.sort_values("stage_id")["time_s"] if "stage_id" in df_a.columns else df_a["time_s"],
        marker=dict(color=color_a, opacity=0.85),
        hovertemplate=f"<b>{name_a}</b><br>Etapa: %{{x}}<br>Tiempo: %{{y:.3f}}s<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name=name_b,
        x=df_b.sort_values("stage_id")["stage_code"] if "stage_id" in df_b.columns else df_b["stage_code"],
        y=df_b.sort_values("stage_id")["time_s"] if "stage_id" in df_b.columns else df_b["time_s"],
        marker=dict(color=color_b, opacity=0.85),
        hovertemplate=f"<b>{name_b}</b><br>Etapa: %{{x}}<br>Tiempo: %{{y:.3f}}s<extra></extra>",
    ))

    layout = _base_layout(
        title=dict(text=f"Comparativa: {name_a} vs {name_b}", font=dict(size=15, color=FONT_COLOR)),
        barmode="group",
        xaxis=dict(
            title="Etapa",
            type="category",
            categoryorder="array",
            categoryarray=stage_order,
            gridcolor=GRID_COLOR,
            tickfont=dict(size=13, color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        yaxis=dict(
            title="Tiempo (s)",
            gridcolor=GRID_COLOR,
            tickfont=dict(color=FONT_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        height=380,
    )
    fig.update_layout(**layout)
    return fig
````

## File: dashboard/pages/01_stages.py
````python
"""Pagina de etapas — tiempos por etapa con selector."""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import streamlit as st

from dashboard.components import api_client as api
from dashboard.components.charts import create_stage_times_chart

st.set_page_config(page_title="Etapas — Rally Analyzer", page_icon="⏱️", layout="wide")

with st.sidebar:
    st.markdown("## Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="Overview")
    st.page_link("pages/01_stages.py", label="Etapas")
    st.page_link("pages/02_evolution.py", label="Evolucion")
    st.page_link("pages/03_compare.py", label="Comparativa")

st.title("Tiempos por Etapa")
st.divider()

stages = api.get_stages()
if not stages:
    st.error("No se puede conectar con la API.")
    st.stop()

stage_options = {f"{s['stage_code']} — {s['name']} ({s['distance_km']} km)": s for s in stages}
selected_label = st.selectbox("Selecciona una etapa", list(stage_options.keys()))
selected_stage = stage_options[selected_label]
stage_id   = selected_stage["stage_id"]
stage_code = selected_stage["stage_code"]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Codigo", stage_code)
with col2:
    st.metric("Distancia", f"{selected_stage['distance_km']} km")
with col3:
    st.metric("Superficie", selected_stage.get("surface", "-"))

st.divider()

result = api.get_stage_times(stage_id)
if not result or not result.get("entries"):
    st.warning("No hay tiempos disponibles para esta etapa.")
    st.stop()

entries = result["entries"]
df = pd.DataFrame(entries)

fig = create_stage_times_chart(df, stage_code)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Tabla de tiempos")
table_rows = []
for e in entries:
    gap  = e.get("diff_first_s", 0) or 0
    prev = e.get("diff_prev_s", 0) or 0
    table_rows.append({
        "Pos.":        e["position"],
        "Piloto":      e["driver_name"],
        "#":           e.get("car_number", ""),
        "Fabricante":  e.get("manufacturer", ""),
        "Tiempo":      e.get("time_str", "-"),
        "Gap lider":   "LIDER" if gap == 0 else f"+{gap:.3f}s",
        "Gap anterior": "—" if prev == 0 else f"+{prev:.3f}s",
    })

st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
````

## File: dashboard/pages/02_evolution.py
````python
"""Pagina de evolucion — bump chart y gap acumulado."""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import streamlit as st

from dashboard.components import api_client as api
from dashboard.components.charts import (
    create_gap_evolution_chart,
    create_position_evolution_chart,
)

st.set_page_config(page_title="Evolucion — Rally Analyzer", page_icon="📈", layout="wide")

with st.sidebar:
    st.markdown("## Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="Overview")
    st.page_link("pages/01_stages.py", label="Etapas")
    st.page_link("pages/02_evolution.py", label="Evolucion")
    st.page_link("pages/03_compare.py", label="Comparativa")

st.title("Evolucion del Rally")
st.divider()

evolution = api.get_evolution()
if not evolution:
    st.error("No se puede conectar con la API.")
    st.stop()

# Construir DataFrame plano
rows = []
for driver in evolution:
    for pos in driver["positions"]:
        rows.append({
            "entry_id":    driver["entry_id"],
            "driver_name": driver["driver_name"],
            "driver_code": driver["driver_code"],
            "manufacturer": driver["manufacturer"],
            "stage_id":    pos["stage_id"],
            "stage_code":  pos["stage_code"],
            "position":    pos["position"],
            "diff_first_s": pos.get("diff_first_s") or 0,
        })

df = pd.DataFrame(rows)

if df.empty or df["stage_code"].str.strip().eq("").all():
    st.warning("No hay datos de evolucion disponibles. Verifica que el pipeline se ejecuto correctamente.")
    st.stop()

# Filtro de pilotos
all_drivers = sorted(df["driver_code"].unique())
selected = st.multiselect("Filtrar pilotos (vacio = todos)", options=all_drivers, default=[])
df_filtered = df[df["driver_code"].isin(selected)] if selected else df

# Bump chart
st.markdown("### Posicion a lo largo del rally")
fig_bump = create_position_evolution_chart(df_filtered)
st.plotly_chart(fig_bump, use_container_width=True)

# Gap chart (excluir lider)
st.markdown("### Gap acumulado respecto al lider")
df_gap = df_filtered[df_filtered["diff_first_s"] > 0].copy()
if df_gap.empty:
    st.info("El lider no tiene gap. Selecciona otros pilotos para ver diferencias.")
else:
    fig_gap = create_gap_evolution_chart(df_gap)
    st.plotly_chart(fig_gap, use_container_width=True)

# Tabla pivot
st.markdown("### Posiciones por etapa")
try:
    stage_order = df_filtered.drop_duplicates("stage_id").sort_values("stage_id")["stage_code"].tolist()
    pivot = df_filtered.pivot_table(
        index=["driver_code", "manufacturer"],
        columns="stage_code",
        values="position",
        aggfunc="first",
    ).reset_index()
    pivot.columns.name = None
    # Reordenar columnas por etapa
    fixed_cols = ["driver_code", "manufacturer"]
    stage_cols = [c for c in stage_order if c in pivot.columns]
    pivot = pivot[fixed_cols + stage_cols]
    st.dataframe(pivot, use_container_width=True, hide_index=True)
except Exception:
    pass
````

## File: dashboard/pages/03_compare.py
````python
"""Pagina de comparativa — dos pilotos cara a cara."""

from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import streamlit as st

from dashboard.components import api_client as api
from dashboard.components.charts import create_comparison_chart

st.set_page_config(page_title="Comparativa — Rally Analyzer", page_icon="🔀", layout="wide")

with st.sidebar:
    st.markdown("## Rally Analyzer")
    st.markdown("---")
    st.page_link("app.py", label="Overview")
    st.page_link("pages/01_stages.py", label="Etapas")
    st.page_link("pages/02_evolution.py", label="Evolucion")
    st.page_link("pages/03_compare.py", label="Comparativa")

st.title("Comparativa entre Pilotos")
st.divider()

drivers = api.get_drivers()
if not drivers:
    st.error("No se puede conectar con la API.")
    st.stop()

driver_options = {
    f"{d['driver_name']} ({d['manufacturer']}) #{d['car_number']}": d
    for d in drivers
}
driver_names = list(driver_options.keys())

col1, col2 = st.columns(2)
with col1:
    sel_a = st.selectbox("Piloto A", driver_names, index=0)
with col2:
    sel_b = st.selectbox("Piloto B", driver_names, index=1)

driver_a = driver_options[sel_a]
driver_b = driver_options[sel_b]

if driver_a["entry_id"] == driver_b["entry_id"]:
    st.warning("Selecciona dos pilotos diferentes.")
    st.stop()

result = api.compare_drivers(driver_a["entry_id"], driver_b["entry_id"])
if not result:
    st.error("No se pudo obtener la comparativa.")
    st.stop()

times_a = result.get("stage_times_a", [])
times_b = result.get("stage_times_b", [])

df_a = pd.DataFrame(times_a)
df_b = pd.DataFrame(times_b)

if df_a.empty or df_b.empty:
    st.warning("No hay datos de tiempos disponibles.")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown(f"### {driver_a['driver_name']} vs {driver_b['driver_name']}")

# Calcular victorias por etapa correctamente (un registro por etapa)
df_a_sorted = df_a.sort_values("stage_code").reset_index(drop=True)
df_b_sorted = df_b.sort_values("stage_code").reset_index(drop=True)

wins_a = 0
wins_b = 0
for _, ra in df_a_sorted.iterrows():
    match = df_b_sorted[df_b_sorted["stage_code"] == ra["stage_code"]]
    if not match.empty:
        ta = ra.get("time_s") or 9999
        tb = match.iloc[0].get("time_s") or 9999
        if ta < tb:
            wins_a += 1
        else:
            wins_b += 1

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(f"Etapas ganadas — {driver_a['driver_code']}", wins_a)
with c2:
    st.metric(f"Etapas ganadas — {driver_b['driver_code']}", wins_b)
with c3:
    st.metric("Total etapas", len(df_a_sorted))

st.divider()

# ── Grafico ───────────────────────────────────────────────────────────────────
fig = create_comparison_chart(
    df_a_sorted, df_b_sorted,
    driver_a["driver_name"], driver_b["driver_name"],
    driver_a.get("manufacturer", ""), driver_b.get("manufacturer", ""),
)
st.plotly_chart(fig, use_container_width=True)

# ── Tabla detallada (sin duplicados) ──────────────────────────────────────────
st.markdown("### Detalle por etapa")

rows = []
for _, ra in df_a_sorted.iterrows():
    stage = ra["stage_code"]
    match = df_b_sorted[df_b_sorted["stage_code"] == stage]
    if match.empty:
        continue
    rb = match.iloc[0]
    ta = ra.get("time_s") or 0
    tb = rb.get("time_s") or 0
    diff = round(ta - tb, 3)
    winner = driver_a["driver_code"] if ta < tb else driver_b["driver_code"]
    rows.append({
        "Etapa": stage,
        f"Tiempo {driver_a['driver_code']} (s)": ta,
        f"Tiempo {driver_b['driver_code']} (s)": tb,
        "Diferencia (s)": diff,
        "Ganador": winner,
    })

df_table = pd.DataFrame(rows)
st.dataframe(df_table, use_container_width=True, hide_index=True)
````

## File: docs/bloque-03-dashboard.md
````markdown
# Bloque 3 — Dashboard Streamlit

## Lecciones del Bloque 2

| Problema | Causa | Solución |
|---|---|---|
| `pydantic-settings` no estaba en `requirements.txt` | Se usaba en `config.py` pero faltaba la dependencia | Añadido `pydantic-settings==2.3.0` al `requirements.txt` |
| Archivos del zip no reemplazan los existentes | Windows no sobreescribe sin confirmación | Copiar archivos manualmente en VSCode |

---

## Objetivo

Construir el dashboard interactivo con Streamlit y Plotly que consume el backend
del Bloque 2 y presenta los datos con gráficos interactivos y filtros dinámicos.

---

## Archivos creados / modificados

```
dashboard/
├── app.py                          ← modificado: página overview completa
├── components/
│   ├── api_client.py               ← nuevo: cliente HTTP al backend
│   └── charts.py                  ← nuevo: gráficos Plotly reutilizables
└── pages/
    ├── 01_stages.py               ← nuevo: página de etapas
    ├── 02_evolution.py            ← nuevo: página de evolución
    └── 03_compare.py              ← nuevo: página de comparativa

ingestion/pipeline.py              ← modificado: encoding="utf-8-sig"
backend/app/services/data_loader.py ← modificado: encoding="utf-8-sig"
docs/
└── bloque-03-dashboard.md         ← este archivo
```

---

## Arquitectura del dashboard

```
FastAPI (localhost:8000)
        │  HTTP/JSON
        ▼
api_client.py       → encapsula todas las llamadas al backend
        │  dicts/listas Python
        ▼
pages/*.py          → lógica de UI y transformación a DataFrames
        │  DataFrames Pandas
        ▼
charts.py           → funciones Plotly → figuras
        │  go.Figure
        ▼
st.plotly_chart()   → renderizado en el navegador
```

---

## Páginas del dashboard

### Overview (`app.py`)
- KPIs: nombre del rally, país, nº etapas, nº pilotos
- Tabla de clasificación general final con gaps
- Resumen por fabricante
- Podio (Top 3)

### Etapas (`pages/01_stages.py`)
- Selector dinámico de etapa (código + nombre + distancia)
- KPIs de la etapa: código, distancia, superficie
- Bar chart horizontal con tiempos, coloreado por fabricante
- Gap vs líder anotado en cada barra
- Tabla detallada con gap vs líder y gap vs anterior

### Evolución (`pages/02_evolution.py`)
- Multiselect de pilotos (filtro dinámico)
- Bump chart: posición de cada piloto etapa a etapa (eje Y invertido)
- Gap chart: gap acumulado respecto al líder
- Tabla pivot de posiciones por etapa

### Comparativa (`pages/03_compare.py`)
- Dos selectores de piloto
- KPIs: etapas ganadas por cada piloto
- Grouped bar chart con tiempos por etapa de ambos pilotos
- Tabla detallada con diferencia por etapa y ganador

---

## Componentes reutilizables

### `charts.py`

| Función | Gráfico | Descripción |
|---|---|---|
| `create_stage_times_chart()` | Bar horizontal | Tiempos de etapa con gap anotado |
| `create_gap_evolution_chart()` | Line chart | Gap acumulado respecto al líder |
| `create_position_evolution_chart()` | Bump chart | Posición etapa a etapa |
| `create_comparison_chart()` | Grouped bar | Tiempos de dos pilotos |

### `api_client.py`
Encapsula todas las llamadas HTTP al backend. Si la API no está disponible,
devuelve listas/dicts vacíos en lugar de lanzar excepciones.

---

## Lecciones del Bloque 3

| Problema | Causa | Solución |
|---|---|---|
| `utf-8 codec can't decode byte 0xa1` en dashboard | Windows guardó los CSVs/archivos con encoding cp1252 en lugar de UTF-8 | Usar `encoding="utf-8-sig"` tanto al guardar CSVs (`pipeline.py`) como al leerlos (`data_loader.py`) |
| El fix `encoding="latin-1"` no funcionó | El error seguía diciendo `utf-8 codec` porque Python seguía usando UTF-8 en otro lugar | La solución correcta es `utf-8-sig` en ambos lados (escritura y lectura) |
| `dashboard/app.py` se corrompió al copiarlo del zip | Windows guardó el archivo con cp1252, corrompiendo emojis y caracteres especiales (`é`, `ó`, `ñ`, `─`) | Reescribir el archivo limpio desde terminal con `python -c "open(..., encoding='utf-8')"` o usar VSCode → Save with Encoding → UTF-8 |
| `ModuleNotFoundError: No module named 'dashboard'` | Streamlit ejecuta `app.py` desde dentro de `dashboard/`, por lo que el módulo raíz no está en el path | Añadir al inicio de `app.py`: `sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` |
| `lru_cache` parecía cachear el error de encoding | Al reiniciar Streamlit sin reiniciar la API, la caché del data_loader podía tener estado inconsistente | Reiniciar siempre **ambos** procesos (API + Streamlit) después de cambios en `data_loader.py` |

### Nota sobre encoding en Windows
Windows usa por defecto `cp1252` (Windows-1252) para archivos de texto. Python en Windows también usa este encoding por defecto al abrir archivos sin especificarlo. El BOM de `utf-8-sig` le indica a Windows que el archivo es UTF-8, evitando el problema. **Regla:** siempre especificar `encoding="utf-8-sig"` al leer/escribir CSVs con caracteres especiales en proyectos Python en Windows.

---

## Issues visuales detectados (a corregir en Bloque 4)

| Issue | Descripción |
|---|---|
| Bump chart comprimido | Todos los datos aparecen en una sola columna, el eje X no muestra las etapas |
| Gap chart sin labels | El eje X e Y no muestran valores legibles |
| Bar chart sin nombres | El eje Y del bar chart de etapas no muestra los nombres de los pilotos |
| Comparativa tabla duplicada | El merge de la tabla de comparativa produce filas duplicadas |
| Colores muy llamativos | Rojo/azul intensos no encajan con estética profesional de portfolio |

---

## Validaciones completadas

```
V1 — Dashboard arranca sin errores    ✅
V2 — Overview con clasificación       ✅
V3 — Pagina Etapas con chart          ✅
V4 — Pagina Evolucion                 ✅
V5 — Pagina Comparativa               ✅
GitHub repo creado y subido           ✅
README actualizado                    ✅
```

---

*Siguiente: Bloque 4 — Graficos avanzados y pulido visual.*
````

## File: ingestion/pipeline.py
````python
"""
Pipeline de ingesta de datos WRC.

Uso:
    python -m ingestion.pipeline                  # descarga temporada activa
    python -m ingestion.pipeline --event-id 123   # descarga un evento concreto
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd

from ingestion import wrc_client as client
from ingestion import transformers as tr

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ingestion.pipeline")

# ── Paths ─────────────────────────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = _PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = _PROJECT_ROOT / "data" / "processed"


def _save_json(data: object, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("JSON guardado → %s", path.name)


def _save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    logger.info("CSV guardado → %s (%d filas)", path.name, len(df))


# ── Pasos del pipeline ────────────────────────────────────────────────────────

def step_season() -> list[dict]:
    """Paso 1: descarga y guarda los eventos de la temporada activa."""
    logger.info("── Paso 1: temporada activa ──")
    events = client.get_active_season()
    _save_json(events, RAW_DIR / "season_events.json")
    df = tr.transform_events(events)
    _save_csv(df, PROCESSED_DIR / "events.csv")
    return events


def step_event(event_id: int, event_name: str) -> None:
    """Paso 2: descarga y procesa un evento completo."""
    logger.info("── Paso 2: evento %d (%s) ──", event_id, event_name)
    safe_name = event_name.lower().replace(" ", "_")[:30]

    # — Itinerario + etapas —
    logger.info("  Descargando itinerario...")
    itinerary = client.get_itinerary(event_id)
    _save_json(itinerary, RAW_DIR / f"{safe_name}_itinerary.json")
    stages_df = tr.transform_stages(itinerary)
    _save_csv(stages_df, PROCESSED_DIR / f"{safe_name}_stages.csv")

    if stages_df.empty:
        logger.warning("  No se encontraron etapas para este evento.")
        return

    # — Entradas (pilotos) —
    logger.info("  Descargando pilotos...")
    try:
        entries = client.get_entries(event_id)
        _save_json(entries, RAW_DIR / f"{safe_name}_entries.json")
        entries_df = tr.transform_entries(entries)
        _save_csv(entries_df, PROCESSED_DIR / f"{safe_name}_entries.csv")
    except Exception as e:
        logger.warning("  No se pudieron descargar pilotos: %s", e)
        entries_df = pd.DataFrame()

    # — Tiempos de cada etapa —
    all_stage_times: list[pd.DataFrame] = []
    all_overall: list[pd.DataFrame] = []

    stage_ids = stages_df["stage_id"].tolist()
    logger.info("  Descargando tiempos de %d etapas...", len(stage_ids))

    for stage_id in stage_ids:
        stage_code = stages_df.loc[
            stages_df["stage_id"] == stage_id, "stage_code"
        ].values[0]
        logger.info("    Etapa %s (id=%d)...", stage_code, stage_id)

        try:
            raw_times = client.get_stage_times(event_id, stage_id)
            if raw_times:
                df_times = tr.transform_stage_times(raw_times, stage_id, event_id)
                df_times["stage_code"] = stage_code
                all_stage_times.append(df_times)
        except Exception as e:
            logger.warning("    stage_times %d fallido: %s", stage_id, e)

        try:
            raw_overall = client.get_overall_results(event_id, stage_id)
            if raw_overall:
                df_overall = tr.transform_overall_results(raw_overall, stage_id, event_id)
                df_overall["stage_code"] = stage_code
                all_overall.append(df_overall)
        except Exception as e:
            logger.warning("    overall %d fallido: %s", stage_id, e)

    # — Guardar consolidados —
    if all_stage_times:
        stage_times_df = pd.concat(all_stage_times, ignore_index=True)
        _save_csv(stage_times_df, PROCESSED_DIR / f"{safe_name}_stage_times.csv")

    if all_overall:
        overall_df = pd.concat(all_overall, ignore_index=True)
        _save_csv(overall_df, PROCESSED_DIR / f"{safe_name}_overall.csv")

    logger.info("  Evento %s completado.", event_name)


def run(event_id: int | None = None) -> None:
    """Punto de entrada principal del pipeline."""
    logger.info("═══ Rally Performance Analyzer — Pipeline de ingesta ═══")

    events = step_season()

    if not events:
        logger.error("No se encontraron eventos en la temporada activa.")
        sys.exit(1)

    # Si se especifica un evento concreto, solo descargamos ese
    if event_id is not None:
        match = [e for e in events if e.get("id") == event_id]
        if not match:
            logger.error("Evento %d no encontrado en la temporada activa.", event_id)
            sys.exit(1)
        targets = match
    else:
        # Por defecto: solo el primer evento completado (status=Completed)
        completed = [e for e in events if e.get("status") == "Completed"]
        targets = completed[:1] if completed else events[:1]

    for event in targets:
        eid = event.get("id")
        ename = event.get("name", f"event_{eid}")
        step_event(eid, ename)

    logger.info("═══ Pipeline finalizado ═══")


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WRC data ingestion pipeline")
    parser.add_argument(
        "--event-id",
        type=int,
        default=None,
        help="ID del evento a descargar (por defecto: primer evento completado)",
    )
    args = parser.parse_args()
    run(event_id=args.event_id)
````

## File: README.md
````markdown
# Rally Performance Analyzer

Dashboard interactivo para analizar tiempos y rendimiento en el **World Rally Championship (WRC)**.

> Proyecto de portfolio — Analisis de datos / Motorsport

---

## Stack tecnologico

| Capa | Tecnologia |
|---|---|
| Backend | Python 3.11 · FastAPI · Uvicorn |
| Dashboard | Streamlit |
| Datos | Pandas · Numpy |
| Visualizacion | Plotly |
| Ingesta | httpx + mock data (estructura WRC oficial) |
| Validacion | Pydantic v2 · pydantic-settings |
| Tests | Pytest (51 tests) |
| Deploy | Streamlit Cloud + Render |

---

## Funcionalidades

- Clasificacion general del rally con tiempos y gaps
- Tiempos por etapa con gap vs lider (bar chart interactivo)
- Evolucion de posiciones a lo largo del rally (bump chart)
- Gap acumulado respecto al lider
- Comparativa entre dos pilotos por etapa
- Filtros dinamicos de pilotos
- API REST documentada con Swagger

---

## Arquitectura

```
mock_data / WRC API
      |
      v
ingestion/pipeline.py   (httpx + Pandas)
      |
      v
data/processed/*.csv
      |
      v
backend/ FastAPI        (endpoints REST)
      |
      v
dashboard/ Streamlit    (Plotly charts)
```

---

## Como ejecutar

```bash
# 1. Crear entorno virtual con Python 3.11 (obligatorio)
py -3.11 -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# o: venv\Scripts\activate     # Windows CMD

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar entorno
cp .env.example .env

# 4. Generar datos
WRC_USE_MOCK=true python -m ingestion.pipeline

# 5. Terminal 1 - API
uvicorn backend.app.main:app --reload

# 6. Terminal 2 - Dashboard
streamlit run dashboard/app.py
```

- API Swagger: http://localhost:8000/docs
- Dashboard: http://localhost:8501

---

## Tests

```bash
pytest backend/tests/ -v
# 51 passed
```

---

## Deploy

### Streamlit Cloud (dashboard)
1. Fork o conecta el repo en https://share.streamlit.io
2. Main file: `dashboard/app.py`
3. En Secrets añade: `DASHBOARD_API_URL = "https://tu-api.onrender.com"`

### Render (API)
1. New Web Service desde el repo
2. Build command: `pip install -r requirements.txt && WRC_USE_MOCK=true python -m ingestion.pipeline`
3. Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

---

## Nota sobre los datos

La API oficial `api.wrc.com` fue dada de baja por WRC durante el desarrollo.
Los datos mock siguen la estructura exacta de la API original e incluyen el
Rally Monte Carlo 2024 con 6 pilotos reales, 5 etapas y tiempos basados en
ritmos reales del WRC.

```bash
# Cuando la API real este disponible:
WRC_USE_MOCK=false python -m ingestion.pipeline
```

---

## Problemas conocidos y soluciones

| Problema | Causa | Solucion |
|---|---|---|
| `pydantic-core` falla | Python 3.14 sin wheels | Usar Python 3.11 |
| `SSLError` en pip | Red corporativa | `--trusted-host pypi.org --trusted-host files.pythonhosted.org` |
| `ModuleNotFoundError: backend` | pytest sin root | `conftest.py` vacio en raiz |
| `api.wrc.com` no resuelve | Dominio dado de baja | Mock data incluido en el repo |
| `utf-8 codec can't decode` | Windows encoding | `encoding="utf-8-sig"` en CSVs |

---

## Estado del proyecto

| Bloque | Descripcion | Estado |
|---|---|---|
| 0 | Setup del proyecto | Completado |
| 1 | Ingesta de datos WRC | Completado |
| 2 | Backend FastAPI | Completado |
| 3 | Dashboard base | Completado |
| 4 | Graficos avanzados | Completado |
| 5 | Pulido y deploy | Completado |

---

## Documentacion

Ver `docs/` para la documentacion detallada de cada bloque, lecciones aprendidas
y guia de comandos rapidos.
````
