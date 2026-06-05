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
