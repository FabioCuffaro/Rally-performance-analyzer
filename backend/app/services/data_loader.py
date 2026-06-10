"""
Servicio de carga de datos V3.

Prioridad: SQLite (rally.db) si existe → CSV fallback si no.
Mismas firmas de funciones que V2 — todos los tests y routers
existentes funcionan sin ningun cambio.
"""

from __future__ import annotations

import logging
import sqlite3
from functools import lru_cache
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
_PROJECT_ROOT  = Path(__file__).resolve().parents[3]
_PROCESSED_DIR = _PROJECT_ROOT / "data" / "processed"
_DB_PATH       = _PROJECT_ROOT / "rally.db"

# ── Registro de rallies (CSV fallback) ────────────────────────────────────────
RALLY_REGISTRY: dict[int, str] = {
    1:     "rallye_automobile_monte_carlo",
    89918: "rallye_automobile_monte_carlo_2025",
    90090: "rally_sweden_2025",
}

DEFAULT_EVENT_ID = 1


def get_slug(event_id: int) -> str:
    slug = RALLY_REGISTRY.get(event_id)
    if not slug:
        raise ValueError(f"Event {event_id} no registrado. Disponibles: {list(RALLY_REGISTRY)}")
    return slug


# ── Deteccion de modo ─────────────────────────────────────────────────────────

def _use_db() -> bool:
    """True si rally.db existe y tiene la tabla events con datos."""
    if not _DB_PATH.exists():
        return False
    try:
        with sqlite3.connect(_DB_PATH) as conn:
            count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            return count > 0
    except Exception:
        return False


def _sql(query: str, params: tuple = ()) -> pd.DataFrame:
    """Ejecuta una query SQL y devuelve un DataFrame."""
    with sqlite3.connect(_DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params)


def _load_csv(filename: str) -> pd.DataFrame:
    path = _PROCESSED_DIR / filename
    if not path.exists():
        logger.warning("CSV no encontrado: %s", filename)
        return pd.DataFrame()
    try:
        df = pd.read_csv(path, encoding="utf-8-sig")
        logger.debug("CSV cargado: %s (%d filas)", filename, len(df))
        return df
    except Exception as e:
        logger.error("Error leyendo %s: %s", filename, e)
        return pd.DataFrame()


# ── Funciones publicas (misma API que V2) ─────────────────────────────────────

@lru_cache(maxsize=1)
def get_events() -> pd.DataFrame:
    if _use_db():
        return _sql("SELECT * FROM events ORDER BY date_start")
    return _load_csv("events.csv")


@lru_cache(maxsize=16)
def get_stages(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    if _use_db():
        return _sql("SELECT * FROM stages WHERE event_id = ? ORDER BY stage_id",
                    (event_id,))
    return _load_csv(f"{get_slug(event_id)}_stages.csv")


@lru_cache(maxsize=16)
def get_entries(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    if _use_db():
        return _sql("SELECT * FROM entries WHERE event_id = ? ORDER BY entry_id",
                    (event_id,))
    return _load_csv(f"{get_slug(event_id)}_entries.csv")


@lru_cache(maxsize=16)
def get_stage_times(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    if _use_db():
        return _sql(
            "SELECT * FROM stage_times WHERE event_id = ? ORDER BY stage_id, position",
            (event_id,),
        )
    return _load_csv(f"{get_slug(event_id)}_stage_times.csv")


@lru_cache(maxsize=16)
def get_overall(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    if _use_db():
        return _sql(
            "SELECT * FROM overall_results WHERE event_id = ? ORDER BY stage_id, position",
            (event_id,),
        )
    return _load_csv(f"{get_slug(event_id)}_overall.csv")


# ── Datos enriquecidos ────────────────────────────────────────────────────────

def get_stage_times_enriched(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    """stage_times + datos del piloto via join en entry_id."""
    if _use_db():
        return _sql(
            """
            SELECT st.*, e.driver_name, e.driver_code, e.manufacturer, e.car_number
            FROM stage_times st
            LEFT JOIN entries e ON st.entry_id = e.entry_id AND st.event_id = e.event_id
            WHERE st.event_id = ?
            ORDER BY st.stage_id, st.position
            """,
            (event_id,),
        )
    times   = get_stage_times(event_id).copy()
    entries = get_entries(event_id)[
        ["entry_id", "driver_name", "driver_code", "manufacturer", "car_number"]
    ]
    if times.empty or entries.empty:
        return times
    return times.merge(entries, on="entry_id", how="left")


def get_overall_enriched(event_id: int = DEFAULT_EVENT_ID) -> pd.DataFrame:
    """overall + datos del piloto via join en entry_id."""
    if _use_db():
        return _sql(
            """
            SELECT o.*, e.driver_name, e.driver_code, e.manufacturer, e.car_number
            FROM overall_results o
            LEFT JOIN entries e ON o.entry_id = e.entry_id AND o.event_id = e.event_id
            WHERE o.event_id = ?
            ORDER BY o.stage_id, o.position
            """,
            (event_id,),
        )
    overall = get_overall(event_id).copy()
    entries = get_entries(event_id)[
        ["entry_id", "driver_name", "driver_code", "manufacturer", "car_number"]
    ]
    if overall.empty or entries.empty:
        return overall
    return overall.merge(entries, on="entry_id", how="left")


def clear_cache() -> None:
    """Limpia la cache de todas las funciones."""
    get_events.cache_clear()
    get_stages.cache_clear()
    get_entries.cache_clear()
    get_stage_times.cache_clear()
    get_overall.cache_clear()
    logger.debug("Cache limpiada")
