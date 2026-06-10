# Rally Performance Analyzer

Dashboard interactivo para analizar tiempos y rendimiento en el **World Rally Championship (WRC)**.
Datos reales WRC 2025 scrapeados de eWRC-results.com y Wikipedia. Echa un ojo 🏎️👀

> Proyecto de portfolio — Analisis de datos / Motorsport

---

## Stack tecnologico

| Capa | Tecnologia |
|---|---|
| Frontend | React 18 · TypeScript · Vite · Tailwind CSS · Recharts |
| Backend | Python 3.11 · FastAPI · Uvicorn |
| Dashboard legacy | Streamlit · Plotly |
| Datos | Pandas · Numpy |
| Ingesta | httpx · BeautifulSoup · scraping eWRC + Wikipedia REST API |
| Validacion | Pydantic v2 · pydantic-settings |
| Tests | Pytest (121 tests) |
| Deploy | Vercel (React) + Render (API) |

---

## Funcionalidades

- Clasificacion final del rally con tiempos reales y gaps
- Tiempos por etapa con selector y bar chart por piloto
- Evolucion de posiciones a lo largo del rally (bump chart + gap chart)
- Comparativa H2H entre dos pilotos con tabla de deltas
- Pace (s/km) por etapa coloreado por superficie
- Ranking de pace medio y etapas ganadas por piloto
- Selector de rally (Monte Carlo 2025, Sweden 2025, mock 2024)
- API REST documentada con Swagger
- Datos reales: 62 pilotos Monte Carlo 2025, 57 pilotos Sweden 2025

---

## Arquitectura

```
eWRC-results.com + Wikipedia REST API
         |
         v
ingestion/ewrc_pipeline.py   (httpx + BeautifulSoup + Pandas)
         |
         v
data/processed/*.csv
         |
         v
backend/ FastAPI              (endpoints REST — /drivers, /stages, /rallies)
         |
         v
frontend/ React + Recharts   (SPA — Overview, Stages, Evolution, Compare, Analysis)
```

---

## Como ejecutar localmente

```bash
# 1. Clonar y crear entorno Python 3.11 (obligatorio)
git clone https://github.com/FabioCuffaro/Rally-performance-analyzer
cd rally-performance-analyzer
py -3.11 -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# o: venv\Scripts\activate     # Windows CMD

# 2. Instalar dependencias Python
pip install -r requirements.txt

# 3. Configurar entorno
cp .env.example .env

# 4. (Opcional) Descargar datos reales WRC 2025
python -m ingestion.ewrc_pipeline --event-id 89918 --slug rallye-automobile-monte-carlo-2025
python -m ingestion.ewrc_pipeline --event-id 90090 --slug rally-sweden-2025

# Los datos mock estan incluidos en el repo (no hace falta descargar nada)

# 5. Terminal 1 — API
uvicorn backend.app.main:app --reload
# http://localhost:8000/docs

# 6. Terminal 2 — React frontend
cd frontend
npm install
npm run dev
# http://localhost:3000

# 7. (Opcional) Dashboard Streamlit legacy
streamlit run dashboard/app.py
# http://localhost:8501
```

---

## Tests

```bash
pytest backend/tests/ -v
# 121 passed
```

---

## Deploy

### React → Vercel

1. Conecta el repo en https://vercel.com/new
2. **Root Directory**: `frontend`
3. **Framework Preset**: Vite (autodetectado)
4. **Build Command**: `npm run build`
5. **Output Directory**: `dist`
6. En **Environment Variables** añade:
   ```
   VITE_API_URL = https://rally-performance-analyzer-api.onrender.com
   ```
7. Deploy — Vercel gestiona el `vercel.json` con rewrites para React Router

### FastAPI → Render

1. New Web Service desde el repo en https://render.com
2. **Build Command**: `pip install -r requirements.txt && WRC_USE_MOCK=true python -m ingestion.pipeline`
3. **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**: `PYTHON_VERSION = 3.11.9`
5. Los CSVs reales estan en el repo — disponibles en produccion sin scraping adicional

---

## Datos

| Fuente | Datos | Cobertura |
|---|---|---|
| eWRC-results.com | Clasificacion final, pilotos, tiempos totales | Monte Carlo 2025 (62 pilotos) |
| Wikipedia REST API | Etapas, distancias, ganadores por etapa | Sweden 2025 (18 etapas) |
| Mock data | Datos completos por etapa para todas las metricas | Monte Carlo 2024 (6 pilotos, 5 etapas) |

---

## Problemas conocidos y soluciones

| Problema | Causa | Solucion |
|---|---|---|
| `pydantic-core` falla al instalar | Python 3.14 sin wheels | Usar Python 3.11 |
| `SSLError` en pip | Red corporativa | `--trusted-host pypi.org --trusted-host files.pythonhosted.org` |
| `ModuleNotFoundError: backend` | pytest sin root | `conftest.py` vacio en raiz |
| `api.wrc.com` no resuelve | Dominio dado de baja por WRC | Mock data incluido en el repo |
| `utf-8 codec can't decode` | Windows encoding | `encoding="utf-8-sig"` en CSVs |
| eWRC sin datos HTML | Next.js + Cloudflare Rocket Loader | Scraper hibrido: SSR /final-results + Wikipedia |
| React Router 404 en Vercel | SPA necesita rewrite | `vercel.json` con rewrites a index.html |

---

## Estado del proyecto

| Bloque | Descripcion | Estado |
|---|---|---|
| 0 | Setup del proyecto | Completado |
| 1 | Ingesta de datos WRC | Completado |
| 2 | Backend FastAPI | Completado |
| 3 | Dashboard base Streamlit | Completado |
| 4 | Graficos avanzados Streamlit | Completado |
| 5 | Pulido y deploy V1 | Completado |
| 6 | Scraper eWRC + datos reales | Completado |
| 7 | Nuevos endpoints + metricas V2 | Completado |
| 8 | React: Setup + Layout | Completado |
| 9 | React: Graficos + Paginas | Completado |
| 10 | Pulido visual + deploy V2 | Completado |
