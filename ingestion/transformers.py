"""
Transformadores de datos WRC.

Reciben dicts/listas crudos de la API y devuelven
DataFrames de Pandas limpios y normalizados.
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _ms_to_seconds(ms: int | None) -> float | None:
    """Convierte milisegundos a segundos con 3 decimales."""
    if ms is None:
        return None
    return round(ms / 1000, 3)


def _ms_to_timestr(ms: int | None) -> str | None:
    """Convierte milisegundos a string legible HH:MM:SS.mmm"""
    if ms is None:
        return None
    total_s = ms / 1000
    hours = int(total_s // 3600)
    minutes = int((total_s % 3600) // 60)
    seconds = total_s % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"


# ── Eventos ──────────────────────────────────────────────────────────────────

def transform_events(raw_events: list[dict]) -> pd.DataFrame:
    """
    Normaliza la lista de eventos de la temporada.

    Columnas: event_id, name, status, country, date_start, date_finish.
    """
    rows = []
    for ev in raw_events:
        rally = ev.get("rally", {})
        days = ev.get("eventDays", [])
        date_start = days[0].get("startDate", "") if days else ""
        date_finish = days[-1].get("finishDate", "") if days else ""

        rows.append({
            "event_id": ev.get("id"),
            "name": ev.get("name", ""),
            "status": ev.get("status", ""),
            "country": rally.get("country", {}).get("name", ""),
            "country_iso": rally.get("country", {}).get("iso2", ""),
            "date_start": date_start,
            "date_finish": date_finish,
        })

    df = pd.DataFrame(rows)
    logger.info("Eventos transformados: %d filas", len(df))
    return df


# ── Etapas ───────────────────────────────────────────────────────────────────

def transform_stages(itinerary: dict) -> pd.DataFrame:
    """
    Extrae y aplana todas las etapas del itinerario.

    Columnas: stage_id, stage_code, name, distance_km, surface, leg_name, day.
    """
    rows = []
    legs = itinerary.get("itineraryLegs", [])

    for leg in legs:
        leg_name = leg.get("name", "")
        day = leg.get("startListId", "")
        sections = leg.get("itinerarySections", [])

        for section in sections:
            stages = section.get("stages", [])
            for stage in stages:
                rows.append({
                    "stage_id": stage.get("stageId"),
                    "stage_code": stage.get("code", ""),
                    "name": stage.get("name", ""),
                    "distance_km": stage.get("distance", 0.0),
                    "surface": stage.get("stageType", ""),
                    "leg_name": leg_name,
                    "status": stage.get("status", ""),
                })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna(subset=["stage_id"])
        df["stage_id"] = df["stage_id"].astype(int)
    logger.info("Etapas transformadas: %d filas", len(df))
    return df


# ── Pilotos (entries) ────────────────────────────────────────────────────────

def transform_entries(raw_entries: list[dict]) -> pd.DataFrame:
    """
    Normaliza la lista de pilotos inscritos.

    Columnas: entry_id, driver_name, codriver_name, manufacturer,
              car_number, group, nationality.
    """
    rows = []
    for entry in raw_entries:
        driver = entry.get("driver", {})
        codriver = entry.get("codriver", {})
        rows.append({
            "entry_id": entry.get("entryId"),
            "driver_name": driver.get("fullName", ""),
            "driver_code": driver.get("code", ""),
            "driver_nationality": driver.get("country", {}).get("iso2", ""),
            "codriver_name": codriver.get("fullName", ""),
            "manufacturer": entry.get("manufacturer", {}).get("name", ""),
            "car_number": entry.get("identifier", ""),
            "group": entry.get("group", {}).get("name", ""),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna(subset=["entry_id"])
        df["entry_id"] = df["entry_id"].astype(int)
    logger.info("Pilotos transformados: %d filas", len(df))
    return df


# ── Tiempos de etapa ─────────────────────────────────────────────────────────

def transform_stage_times(
    raw_times: list[dict],
    stage_id: int,
    event_id: int,
) -> pd.DataFrame:
    """
    Normaliza los tiempos de una etapa concreta.

    Columnas: event_id, stage_id, entry_id, position,
              time_ms, time_s, time_str, diff_first_ms, diff_first_s, status.
    """
    rows = []
    for t in raw_times:
        rows.append({
            "event_id": event_id,
            "stage_id": stage_id,
            "entry_id": t.get("entryId"),
            "position": t.get("position"),
            "time_ms": t.get("elapsedDurationMs"),
            "time_s": _ms_to_seconds(t.get("elapsedDurationMs")),
            "time_str": _ms_to_timestr(t.get("elapsedDurationMs")),
            "diff_first_ms": t.get("diffFirstMs"),
            "diff_first_s": _ms_to_seconds(t.get("diffFirstMs")),
            "diff_prev_ms": t.get("diffPrevMs"),
            "diff_prev_s": _ms_to_seconds(t.get("diffPrevMs")),
            "status": t.get("status", ""),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna(subset=["entry_id"])
        df["entry_id"] = df["entry_id"].astype(int)
        df = df.sort_values("position").reset_index(drop=True)
    logger.info(
        "Stage times transformados: event=%d stage=%d → %d filas",
        event_id, stage_id, len(df)
    )
    return df


# ── Clasificación general ────────────────────────────────────────────────────

def transform_overall_results(
    raw_results: list[dict],
    stage_id: int,
    event_id: int,
) -> pd.DataFrame:
    """
    Normaliza la clasificación general acumulada tras una etapa.

    Columnas: event_id, stage_id, entry_id, position,
              total_time_ms, total_time_s, total_time_str,
              diff_first_ms, diff_first_s.
    """
    rows = []
    for r in raw_results:
        rows.append({
            "event_id": event_id,
            "stage_id": stage_id,
            "entry_id": r.get("entryId"),
            "position": r.get("position"),
            "total_time_ms": r.get("totalTimeMs"),
            "total_time_s": _ms_to_seconds(r.get("totalTimeMs")),
            "total_time_str": _ms_to_timestr(r.get("totalTimeMs")),
            "diff_first_ms": r.get("diffFirstMs"),
            "diff_first_s": _ms_to_seconds(r.get("diffFirstMs")),
            "status": r.get("penaltyTimeMs", "OK"),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.dropna(subset=["entry_id"])
        df["entry_id"] = df["entry_id"].astype(int)
        df = df.sort_values("position").reset_index(drop=True)
    logger.info(
        "Overall results transformados: event=%d stage=%d → %d filas",
        event_id, stage_id, len(df)
    )
    return df
