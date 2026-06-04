# 🏁 Rally Performance Analyzer

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
| Ingesta | httpx (WRC Live Timing API) |
| Tests | Pytest |

---

## Funcionalidades (MVP)

- 📊 Clasificación general del rally
- ⏱️ Tiempos por etapa con gap vs líder
- 📈 Evolución de posiciones a lo largo del rally
- 🔀 Comparativa entre dos pilotos
- 🎛️ Filtros dinámicos por rally y temporada

---

## Arquitectura

```
WRC API → Ingesta (httpx + Pandas) → data/processed/ → FastAPI → Streamlit + Plotly
```

---

## Cómo ejecutar

```bash
# Instalar dependencias
make install
source venv/bin/activate

# Terminal 1 — API
make run-api        # http://localhost:8000/docs

# Terminal 2 — Dashboard
make run-dashboard  # http://localhost:8501
```

---

## Tests

```bash
make test
```

---

## Estado del proyecto

| Bloque | Descripción | Estado |
|---|---|---|
| 0 | Setup del proyecto | ✅ Completado |
| 1 | Ingesta de datos WRC | ⏳ Pendiente |
| 2 | Backend FastAPI | ⏳ Pendiente |
| 3 | Dashboard base | ⏳ Pendiente |
| 4 | Gráficos avanzados | ⏳ Pendiente |
| 5 | Pulido y deploy | ⏳ Pendiente |

---

## Documentación

Ver [`docs/`](docs/) para la documentación detallada de cada bloque.
