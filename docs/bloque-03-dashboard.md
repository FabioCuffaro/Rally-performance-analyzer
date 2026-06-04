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

### 🏠 Overview (`app.py`)
- KPIs: nombre del rally, país, nº etapas, nº pilotos
- Tabla de clasificación general final con gaps
- Resumen por fabricante
- Podio (Top 3)

### ⏱️ Etapas (`pages/01_stages.py`)
- Selector dinámico de etapa (código + nombre + distancia)
- KPIs de la etapa: código, distancia, superficie
- Bar chart horizontal con tiempos, coloreado por fabricante
- Gap vs líder anotado en cada barra
- Tabla detallada con gap vs líder y gap vs anterior

### 📈 Evolución (`pages/02_evolution.py`)
- Multiselect de pilotos (filtro dinámico)
- Bump chart: posición de cada piloto etapa a etapa (eje Y invertido)
- Gap chart: gap acumulado respecto al líder
- Tabla pivot de posiciones por etapa

### 🔀 Comparativa (`pages/03_compare.py`)
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

Todas las funciones reciben un DataFrame y devuelven un `go.Figure`.
Los colores se asignan por fabricante (Toyota=rojo, Hyundai=azul).

### `api_client.py`

Encapsula todas las llamadas HTTP al backend. Si la API no está disponible,
devuelve listas/dicts vacíos en lugar de lanzar excepciones.

---

## Cómo ejecutar el dashboard

Con el backend ya corriendo en el terminal 1:

```bash
# Terminal 2 — desde la raíz del proyecto
streamlit run dashboard/app.py
```

Abre → `http://localhost:8501`

---

## Validaciones del Bloque 3

### V1 — Dashboard arranca sin errores
```
streamlit run dashboard/app.py
→ http://localhost:8501 visible en el navegador
```

### V2 — Overview muestra clasificación
```
http://localhost:8501
→ Tabla con 6 pilotos, KPIs del rally visibles
```

### V3 — Página Etapas funciona
```
http://localhost:8501/01_stages
→ Selector de etapa + bar chart + tabla
```

### V4 — Página Evolución funciona
```
http://localhost:8501/02_evolution
→ Bump chart y gap chart visibles
→ Filtro multiselect de pilotos reactivo
```

### V5 — Página Comparativa funciona
```
http://localhost:8501/03_compare
→ Selectores de piloto + grouped bar chart + tabla
```

---

## Posibles errores comunes

| Error | Causa | Solución |
|---|---|---|
| `⚠️ No se puede conectar con la API` | FastAPI no está corriendo | Arrancar con `uvicorn backend.app.main:app --reload` |
| `ModuleNotFoundError: dashboard` | Streamlit no encuentra el módulo | Ejecutar desde la raíz del proyecto |
| Gráfico vacío | `df` está vacío | Verificar que se ejecutó el pipeline del Bloque 1 |
| `st.page_link` error | Versión de Streamlit antigua | Verificar `streamlit==1.35.0` |

---

*Siguiente: Bloque 4 — Gráficos avanzados y pulido visual.*
