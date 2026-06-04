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
