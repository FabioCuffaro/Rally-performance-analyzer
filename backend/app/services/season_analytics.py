"""
Analitica de temporada — Bloque 12.

Agrega metricas de multiples rallies para ver la temporada completa.
Las funciones usan driver_name como clave de cruce entre eventos
(no entry_id, que es unico por evento).
"""

from __future__ import annotations

import logging

import pandas as pd

from backend.app.services import data_loader as loader
from backend.app.services.analytics import (
    get_final_classification,
    calculate_pace,
)

logger = logging.getLogger(__name__)

# ── Puntos FIA WRC (posicion → puntos) ───────────────────────────────────────
FIA_POINTS: dict[int, int] = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
    6: 8,  7: 6,  8: 4,  9: 2,  10: 1,
}

# Eventos reales WRC 2025 disponibles (default para endpoints de temporada)
DEFAULT_SEASON_EVENTS = [89918, 90090]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _event_name(event_id: int) -> str:
    events_df = loader.get_events()
    row = events_df[events_df["event_id"] == event_id]
    return str(row.iloc[0]["name"]) if not row.empty else str(event_id)


def _parse_event_ids(event_ids: list[int] | None) -> list[int]:
    if not event_ids:
        return DEFAULT_SEASON_EVENTS
    return [eid for eid in event_ids if eid in loader.RALLY_REGISTRY]


# ── Standings ─────────────────────────────────────────────────────────────────

def get_season_standings(event_ids: list[int] | None = None) -> pd.DataFrame:
    """
    Puntos FIA acumulados por piloto en la temporada.

    Devuelve DataFrame con columnas:
      driver_name, manufacturer, total_points,
      + una columna por rally: points_{event_id}
    """
    ids = _parse_event_ids(event_ids)
    all_rows: list[dict] = []

    for event_id in ids:
        classification = get_final_classification(event_id)
        if classification.empty:
            logger.warning("Sin clasificacion para event_id=%d", event_id)
            continue

        event_name = _event_name(event_id)
        for _, row in classification.iterrows():
            pos = int(row["position"])
            points = FIA_POINTS.get(pos, 0)
            all_rows.append({
                "driver_name":  str(row.get("driver_name", "")),
                "manufacturer": str(row.get("manufacturer", "")),
                "event_id":     event_id,
                "event_name":   event_name,
                "position":     pos,
                "points":       points,
            })

    if not all_rows:
        return pd.DataFrame()

    df = pd.DataFrame(all_rows)

    # Tabla pivot: driver_name | points_89918 | points_90090 | total
    pivot = df.pivot_table(
        index=["driver_name", "manufacturer"],
        columns="event_id",
        values="points",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()

    # Renombrar columnas de puntos por event_id
    pivot.columns = [
        f"points_{c}" if isinstance(c, int) else c
        for c in pivot.columns
    ]

    # Calcular total
    pts_cols = [c for c in pivot.columns if c.startswith("points_")]
    pivot["total_points"] = pivot[pts_cols].sum(axis=1)

    pivot = pivot[pivot["total_points"] > 0]
    return pivot.sort_values("total_points", ascending=False).reset_index(drop=True)


# ── Pace evolution ─────────────────────────────────────────────────────────────

def get_season_pace_evolution(event_ids: list[int] | None = None) -> pd.DataFrame:
    """
    Pace medio por piloto y rally.

    Devuelve DataFrame con columnas:
      driver_name, manufacturer, event_id, event_name, avg_pace, stage_count
    """
    ids = _parse_event_ids(event_ids)
    rows: list[dict] = []

    for event_id in ids:
        pace_df = calculate_pace(event_id)
        if pace_df.empty:
            logger.info("Sin pace para event_id=%d", event_id)
            continue

        event_name = _event_name(event_id)
        summary = (
            pace_df.groupby(["driver_name", "manufacturer"])["pace_s_per_km"]
            .agg(avg_pace="mean", stage_count="count")
            .reset_index()
        )
        summary["event_id"]   = event_id
        summary["event_name"] = event_name
        summary["avg_pace"]   = summary["avg_pace"].round(3)
        rows.append(summary)

    if not rows:
        return pd.DataFrame()

    return pd.concat(rows, ignore_index=True)


# ── Surface mastery ───────────────────────────────────────────────────────────

def get_season_surface_mastery(event_ids: list[int] | None = None) -> pd.DataFrame:
    """
    Pace medio por piloto y superficie a lo largo de la temporada.

    Devuelve DataFrame con columnas:
      driver_name, manufacturer, surface, avg_pace, stage_count, rally_count
    """
    ids = _parse_event_ids(event_ids)
    rows: list[dict] = []

    for event_id in ids:
        pace_df = calculate_pace(event_id)
        if pace_df.empty:
            continue
        pace_df["event_id"] = event_id
        rows.append(pace_df)

    if not rows:
        return pd.DataFrame()

    df = pd.concat(rows, ignore_index=True)

    agg = (
        df.groupby(["driver_name", "manufacturer", "surface"])
        .agg(
            avg_pace=("pace_s_per_km", "mean"),
            stage_count=("pace_s_per_km", "count"),
            rally_count=("event_id", "nunique"),
        )
        .reset_index()
    )
    agg["avg_pace"] = agg["avg_pace"].round(3)
    return agg.sort_values(["surface", "avg_pace"]).reset_index(drop=True)


# ── Head-to-head temporada ────────────────────────────────────────────────────

def get_season_h2h(
    driver_a: str,
    driver_b: str,
    event_ids: list[int] | None = None,
) -> pd.DataFrame:
    """
    Comparativa entre dos pilotos a lo largo de la temporada.

    Devuelve DataFrame con columnas:
      event_id, event_name, position_a, position_b,
      points_a, points_b, winner (A/B/Tie)
    """
    ids = _parse_event_ids(event_ids)
    rows: list[dict] = []

    for event_id in ids:
        classification = get_final_classification(event_id)
        if classification.empty:
            continue

        event_name = _event_name(event_id)

        def _find(name: str) -> tuple[int | None, int]:
            row = classification[
                classification["driver_name"].str.strip().str.lower()
                == name.strip().lower()
            ]
            if row.empty:
                return None, 0
            pos = int(row.iloc[0]["position"])
            return pos, FIA_POINTS.get(pos, 0)

        pos_a, pts_a = _find(driver_a)
        pos_b, pts_b = _find(driver_b)

        winner = "Tie"
        if pos_a is not None and pos_b is not None:
            winner = "A" if pos_a < pos_b else ("B" if pos_b < pos_a else "Tie")
        elif pos_a is not None:
            winner = "A"
        elif pos_b is not None:
            winner = "B"

        rows.append({
            "event_id":   event_id,
            "event_name": event_name,
            "position_a": pos_a,
            "position_b": pos_b,
            "points_a":   pts_a,
            "points_b":   pts_b,
            "winner":     winner,
        })

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)
