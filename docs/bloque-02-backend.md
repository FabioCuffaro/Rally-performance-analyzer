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
