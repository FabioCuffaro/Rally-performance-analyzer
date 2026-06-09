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
| Ingesta | httpx · BeautifulSoup · scraping eWRC + Wikipedia |
| Validacion | Pydantic v2 · pydantic-settings |
| Tests | Pytest (89 tests) |
| Deploy | Streamlit Cloud + Render |

---

## Funcionalidades

- Clasificacion general del rally con tiempos y gaps reales
- Tiempos por etapa con gap vs lider (bar chart interactivo)
- Evolucion de posiciones a lo largo del rally (bump chart)
- Gap acumulado respecto al lider
- Comparativa entre dos pilotos por etapa
- Filtros dinamicos de pilotos
- API REST documentada con Swagger
- Datos reales WRC 2025 (Monte Carlo, Sweden)

---

## Arquitectura

```
eWRC-results.com + Wikipedia
         |
         v
ingestion/ewrc_pipeline.py   (httpx + BeautifulSoup + Pandas)
         |
         v
data/processed/*.csv
         |
         v
backend/ FastAPI              (endpoints REST)
         |
         v
dashboard/ Streamlit          (Plotly charts)
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

# 4. Descargar datos reales WRC 2025
python -m ingestion.ewrc_pipeline --event-id 89918 --slug rallye-automobile-monte-carlo-2025
python -m ingestion.ewrc_pipeline --event-id 90090 --slug rally-sweden-2025

# (Alternativa: datos mock incluidos en el repo)
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
# 89 passed
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

## Datos

Los datos provienen de dos fuentes:

- **eWRC-results.com** — resultados finales y clasificaciones WRC 2025 via scraping
- **Wikipedia REST API** — etapas, distancias y ganadores de etapa

Los CSVs generados cubren Monte Carlo 2025 (62 pilotos) y Rally Sweden 2025 (57 pilotos, 18 etapas).
Los datos mock del Rally Monte Carlo 2024 siguen incluidos como fallback.

---

## Problemas conocidos y soluciones

| Problema | Causa | Solucion |
|---|---|---|
| `pydantic-core` falla | Python 3.14 sin wheels | Usar Python 3.11 |
| `SSLError` en pip | Red corporativa | `--trusted-host pypi.org --trusted-host files.pythonhosted.org` |
| `ModuleNotFoundError: backend` | pytest sin root | `conftest.py` vacio en raiz |
| `api.wrc.com` no resuelve | Dominio dado de baja | Mock data incluido en el repo |
| `utf-8 codec can't decode` | Windows encoding | `encoding="utf-8-sig"` en CSVs |
| eWRC Next.js sin datos | Cloudflare Rocket Loader bloquea JS | Scraper hibrido: SSR /final-results + Wikipedia |

---

## Estado del proyecto

| Bloque | Descripcion | Estado |
|---|---|---|
| 0 | Setup del proyecto | Completado |
| 1 | Ingesta de datos WRC | Completado |
| 2 | Backend FastAPI | Completado |
| 3 | Dashboard base | Completado |
| 4 | Graficos avanzados | Completado |
| 5 | Pulido y deploy V1 | Completado |
| 6 | Scraper eWRC + datos reales | Completado |
| 7 | Nuevos endpoints + metricas | Pendiente |
| 8 | React: Setup + Layout | Pendiente |
| 9 | React: Graficos + Paginas | Pendiente |
| 10 | Pulido visual + deploy V2 | Pendiente |
