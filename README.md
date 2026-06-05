# Rally Performance Analyzer

Dashboard interactivo para analizar tiempos y rendimiento en el **World Rally Championship (WRC)**.

> Proyecto de portfolio — Análisis de datos / Motorsport

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | Python · FastAPI · Uvicorn |
| Dashboard | Streamlit |
| Datos | Pandas · Numpy |
| Visualización | Plotly |
| Ingesta | httpx + mock data (estructura WRC oficial) |
| Validación | Pydantic v2 |
| Tests | Pytest |

---

## Funcionalidades

- Clasificación general del rally con tiempos y gaps
- Tiempos por etapa con gap vs líder (bar chart interactivo)
- Evolución de posiciones a lo largo del rally (bump chart)
- Gap acumulado respecto al líder
- Comparativa entre dos pilotos por etapa
- Filtros dinámicos de pilotos
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

## Cómo ejecutar

```bash
# 1. Crear entorno virtual con Python 3.11 (obligatorio)
py -3.11 -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# o: venv\Scripts\activate     # Windows CMD

# 2. Instalar dependencias
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# 3. Configurar entorno
cp .env.example .env

# 4. Generar datos
WRC_USE_MOCK=true python -m ingestion.pipeline

# 5. Terminal 1 — API
uvicorn backend.app.main:app --reload

# 6. Terminal 2 — Dashboard
streamlit run dashboard/app.py
```

- API: http://localhost:8000/docs
- Dashboard: http://localhost:8501

---

## Tests

```bash
pytest backend/tests/ -v
# 51 tests passed
```

---

## Nota sobre los datos

La API oficial `api.wrc.com` fue dada de baja por WRC durante el desarrollo.
Los datos mock siguen la estructura exacta de la API original e incluyen el
Rally Monte Carlo 2024 con 6 pilotos reales, 5 etapas y tiempos basados en
ritmos reales del WRC (~1 min/km en tarmac).

Para usar datos reales cuando la API vuelva a estar disponible:
```bash
WRC_USE_MOCK=false python -m ingestion.pipeline
```

---

## Problemas conocidos y soluciones

| Problema | Causa | Solución |
|---|---|---|
| `pydantic-core` falla al instalar | Python 3.14 sin wheels | Usar Python 3.11 |
| `SSLError` en pip | Red corporativa con proxy | `--trusted-host pypi.org --trusted-host files.pythonhosted.org` |
| `ModuleNotFoundError: backend` en pytest | pytest no encuentra el root | `conftest.py` vacío en raíz + `backend/__init__.py` |
| `api.wrc.com` no resuelve | Dominio dado de baja | Mock data con estructura idéntica |
| `WRC_USE_MOCK` ignorado | `.env` se carga tarde | Pasar inline: `WRC_USE_MOCK=true python -m ...` |
| `utf-8 codec can't decode` en dashboard | Windows guarda archivos como cp1252 | Guardar archivos Python con encoding UTF-8 explícito |
| `ModuleNotFoundError: dashboard` en Streamlit | Streamlit ejecuta desde subcarpeta | `sys.path.insert` al inicio de `app.py` |

---

## Estado del proyecto

| Bloque | Descripción | Estado |
|---|---|---|
| 0 | Setup del proyecto | Completado |
| 1 | Ingesta de datos WRC | Completado |
| 2 | Backend FastAPI | Completado |
| 3 | Dashboard base | Completado |
| 4 | Gráficos avanzados | Pendiente |
| 5 | Pulido y deploy | Pendiente |

---

## Documentación

Ver `docs/` para la documentación detallada de cada bloque implementado.
