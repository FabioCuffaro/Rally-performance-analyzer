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
