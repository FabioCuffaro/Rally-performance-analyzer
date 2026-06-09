"""
Servicio de carga de datos — multi-rally (V2).

Mapea event_id -> slug -> CSVs en data/processed/.
DEFAULT_EVENT_ID=1 mantiene backward compat con tests existentes (mock V1).
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_PROCESSED_DIR = _PROJECT_ROOT / "data" / "processed"

# ── Registro de rallies disponibles ───────────────────────────────────────────
# event_id -> slug de ficheros CSV en data/processed/
RALLY_REGISTRY: dict[int, str] = {
    1:     "rallye_automobile_monte_carlo",           # mock V1 (6 pilotos)
    89918: "rallye_automobile_monte_carlo_2025",      # real eWRC (62 pilotos)
    90090: "rally_sweden_2025",                       # real Wikipedia (57 pilotos)
}

DEFAULT_EVENT_ID = 1  # mock — backward compat con todos los tests existentes


def get_slug(event_id: int) -> str:
    """Devuelve el slug de ficheros para un event_id."""
    slug = RALLY_REGISTRY.get(event_id)
    if not slug:
        raise ValueError(f"Event {event_id} no registrado. Disponibles: {list(RALLY_REGISTRY)}")
    return slug


def _load_csv(filename: str) -> pd.DataFrame:
    path = _PROCESSED_DIR / filename
    if not path.exists():
        logger.warning("CSV no encontrado: %s", filename)
        return pd.DataFrame()
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
        logger.info("CSV cargado: %s (%d filas)", filename, len(df))
        return df
    except Exception as e:
        logger.error("Error leyendo %s: %s", filename, e)
        return pd.DataFrame()


# ── Carga de datos (con cache por event_id) ───────────────────────────────────

@lru_cache(maxsize=1)
def get_events() -> pd.DataFrame:
    return _load_csv("events.csv")


@lru_cache(maxsize=8)
def get_stages(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    return _load_csv(f"{get_slug(event_id)}_stages.csv")


@lru_cache(maxsize=8)
def get_entries(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    return _load_csv(f"{get_slug(event_id)}_entries.csv")


@lru_cache(maxsize=8)
def get_stage_times(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    return _load_csv(f"{get_slug(event_id)}_stage_times.csv")


@lru_cache(maxsize=8)
def get_overall(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    return _load_csv(f"{get_slug(event_id)}_overall.csv")


# ── Datos enriquecidos ────────────────────────────────────────────────────────

def get_stage_times_enriched(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    """stage_times + datos del piloto via join en entry_id."""
    times = get_stage_times(event_id).copy()
    entries = get_entries(event_id)[
        ["entry_id", "driver_name", "driver_code", "manufacturer", "car_number"]
    ]
    if times.empty or entries.empty:
        return times
    return times.merge(entries, on="entry_id", how="left")


def get_overall_enriched(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    """overall + datos del piloto via join en entry_id."""
    overall = get_overall(event_id).copy()
    entries = get_entries(event_id)[
        ["entry_id", "driver_name", "driver_code", "manufacturer", "car_number"]
    ]
    if overall.empty or entries.empty:
        return overall
    return overall.merge(entries, on="entry_id", how="left")


def clear_cache() -> None:
    """Limpia toda la cache (util para tests y recarga)."""
    get_events.cache_clear()
    get_stages.cache_clear()
    get_entries.cache_clear()
    get_stage_times.cache_clear()
    get_overall.cache_clear()
    logger.info("Cache limpiada")
