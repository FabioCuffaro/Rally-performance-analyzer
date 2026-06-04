"""
Servicio de carga de datos.

Carga los CSVs procesados como DataFrames de Pandas y los cachea en memoria.
Se inicializa una sola vez al arrancar la API.
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

# Prefijo del evento principal (Monte Carlo)
_EVENT_PREFIX = "rallye_automobile_monte_carlo"


def _load_csv(filename: str) -> pd.DataFrame:
    """Carga un CSV desde data/processed/ con manejo de errores."""
    path = _PROCESSED_DIR / filename
    if not path.exists():
        logger.warning("CSV no encontrado: %s — devolviendo DataFrame vacío", filename)
        return pd.DataFrame()
    df = pd.read_csv(path, encoding="utf-8-sig")
    logger.info("CSV cargado: %s (%d filas)", filename, len(df))
    return df


# ── Carga de datos ────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def get_events() -> pd.DataFrame:
    """Devuelve los eventos de la temporada."""
    return _load_csv("events.csv")


@lru_cache(maxsize=1)
def get_stages() -> pd.DataFrame:
    """Devuelve las etapas del rally principal."""
    return _load_csv(f"{_EVENT_PREFIX}_stages.csv")


@lru_cache(maxsize=1)
def get_entries() -> pd.DataFrame:
    """Devuelve los pilotos inscritos."""
    return _load_csv(f"{_EVENT_PREFIX}_entries.csv")


@lru_cache(maxsize=1)
def get_stage_times() -> pd.DataFrame:
    """Devuelve todos los tiempos de etapa."""
    return _load_csv(f"{_EVENT_PREFIX}_stage_times.csv")


@lru_cache(maxsize=1)
def get_overall() -> pd.DataFrame:
    """Devuelve la clasificación general acumulada."""
    return _load_csv(f"{_EVENT_PREFIX}_overall.csv")


def get_stage_times_enriched() -> pd.DataFrame:
    """
    Devuelve tiempos de etapa enriquecidos con datos del piloto.

    Join entre stage_times y entries por entry_id.
    """
    times = get_stage_times().copy()
    entries = get_entries()[
        ["entry_id", "driver_name", "driver_code", "manufacturer", "car_number"]
    ]
    if times.empty or entries.empty:
        return times
    return times.merge(entries, on="entry_id", how="left")


def get_overall_enriched() -> pd.DataFrame:
    """
    Devuelve clasificación general enriquecida con datos del piloto.
    """
    overall = get_overall().copy()
    entries = get_entries()[
        ["entry_id", "driver_name", "driver_code", "manufacturer", "car_number"]
    ]
    if overall.empty or entries.empty:
        return overall
    return overall.merge(entries, on="entry_id", how="left")


def clear_cache() -> None:
    """Limpia la caché (útil para tests o recarga de datos)."""
    get_events.cache_clear()
    get_stages.cache_clear()
    get_entries.cache_clear()
    get_stage_times.cache_clear()
    get_overall.cache_clear()
    logger.info("Caché de datos limpiada")
