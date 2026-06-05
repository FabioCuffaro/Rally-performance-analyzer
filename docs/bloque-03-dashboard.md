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
