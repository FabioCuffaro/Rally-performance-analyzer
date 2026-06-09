"""
Servicio de analitica — V2.

Funciones existentes actualizadas para multi-rally (event_id param).
Nuevas metricas: pace, surface stats, consistency, stage wins, momentum.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from backend.app.services import data_loader as loader

logger = logging.getLogger(__name__)

_DEFAULT = loader.DEFAULT_EVENT_ID


# ── Funciones existentes (ahora con event_id) ─────────────────────────────────

def get_stage_result(stage_id: int, event_id: int = _DEFAULT) -> pd.DataFrame:
    df = loader.get_stage_times_enriched(event_id)
    if df.empty:
        return df
    return df[df["stage_id"] == stage_id].sort_values("position").reset_index(drop=True)


def get_overall_at_stage(stage_id: int, event_id: int = _DEFAULT) -> pd.DataFrame:
    df = loader.get_overall_enriched(event_id)
    if df.empty:
        return df
    return df[df["stage_id"] == stage_id].sort_values("position").reset_index(drop=True)


def get_final_classification(event_id: int = _DEFAULT) -> pd.DataFrame:
    df = loader.get_overall_enriched(event_id)
    if df.empty:
        return df
    last_stage = df["stage_id"].max()
    return get_overall_at_stage(last_stage, event_id)


def get_driver_evolution(entry_id: int, event_id: int = _DEFAULT) -> pd.DataFrame:
    df = loader.get_overall_enriched(event_id)
    if df.empty:
        return df
    if "stage_code" not in df.columns:
        stages = loader.get_stages(event_id)[["stage_id", "stage_code"]]
        df = df.merge(stages, on="stage_id", how="left")
    return df[df["entry_id"] == entry_id].sort_values("stage_id").reset_index(drop=True)


def get_all_drivers_evolution(event_id: int = _DEFAULT) -> pd.DataFrame:
    df = loader.get_overall_enriched(event_id)
    if df.empty:
        return df
    if "stage_code" not in df.columns:
        stages = loader.get_stages(event_id)[["stage_id", "stage_code"]]
        df = df.merge(stages, on="stage_id", how="left")
    return df.sort_values(["entry_id", "stage_id"]).reset_index(drop=True)


def get_driver_comparison(entry_id_a: int, entry_id_b: int, event_id: int = _DEFAULT) -> dict:
    times = loader.get_stage_times_enriched(event_id)

    def _get(eid: int) -> pd.DataFrame:
        df = times[times["entry_id"] == eid].copy()
        if "stage_code" not in df.columns:
            stages = loader.get_stages(event_id)[["stage_id", "stage_code"]]
            df = df.merge(stages, on="stage_id", how="left")
        return df.sort_values("stage_id").reset_index(drop=True)

    return {"driver_a": _get(entry_id_a), "driver_b": _get(entry_id_b)}


# ── Nuevas metricas V2 ────────────────────────────────────────────────────────

def calculate_pace(event_id: int = _DEFAULT) -> pd.DataFrame:
    """
    Pace por piloto y etapa: pace_s_per_km = time_s / distance_km.

    Requiere stage_times y stages con distance_km.
    Devuelve DataFrame con columnas:
      entry_id, driver_name, stage_code, time_s, distance_km, pace_s_per_km, surface
    """
    times = loader.get_stage_times_enriched(event_id)
    stages = loader.get_stages(event_id)[["stage_id", "stage_code", "distance_km", "surface"]]

    if times.empty or stages.empty:
        logger.warning("Sin datos para calcular pace (event_id=%d)", event_id)
        return pd.DataFrame()

    if stages.empty or "stage_id" not in stages.columns:
        logger.warning("Stages sin datos para pace (event_id=%d)", event_id)
        return pd.DataFrame()

    df = times.merge(stages, on="stage_id", how="left")

    # Evitar division por cero
    df = df[df["distance_km"] > 0].copy()
    df["pace_s_per_km"] = (df["time_s"] / df["distance_km"]).round(3)

    # Usar stage_code_x si hay duplicado de merge
    if "stage_code_x" in df.columns:
        df = df.rename(columns={"stage_code_x": "stage_code"}).drop(
            columns=["stage_code_y"], errors="ignore"
        )

    cols = ["entry_id", "driver_name", "driver_code", "manufacturer",
            "stage_id", "stage_code", "time_s", "distance_km", "pace_s_per_km", "surface"]
    return df[[c for c in cols if c in df.columns]].reset_index(drop=True)


def get_surface_analysis(event_id: int = _DEFAULT) -> pd.DataFrame:
    """
    Media de pace agrupada por piloto y superficie.

    Devuelve DataFrame con:
      entry_id, driver_name, surface, avg_pace, stage_count
    """
    pace_df = calculate_pace(event_id)
    if pace_df.empty:
        return pd.DataFrame()

    group_cols = ["entry_id", "driver_name", "surface"]
    agg = (
        pace_df.groupby(group_cols)["pace_s_per_km"]
        .agg(avg_pace="mean", stage_count="count")
        .reset_index()
    )
    agg["avg_pace"] = agg["avg_pace"].round(3)
    return agg.sort_values(["entry_id", "surface"]).reset_index(drop=True)


def calculate_consistency(event_id: int = _DEFAULT) -> pd.DataFrame:
    """
    Consistencia por piloto: desviacion estandar del pace entre etapas.

    Menor std = mas consistente.
    Devuelve DataFrame con:
      entry_id, driver_name, manufacturer, pace_mean, pace_std, stage_count
    """
    pace_df = calculate_pace(event_id)
    if pace_df.empty:
        return pd.DataFrame()

    group_cols = ["entry_id", "driver_name", "manufacturer"]
    agg = (
        pace_df.groupby(group_cols)["pace_s_per_km"]
        .agg(
            pace_mean="mean",
            pace_std=lambda x: float(np.std(x, ddof=0)) if len(x) > 0 else 0.0,
            stage_count="count",
        )
        .reset_index()
    )
    agg["pace_mean"] = agg["pace_mean"].round(3)
    agg["pace_std"] = agg["pace_std"].round(3)
    return agg.sort_values("pace_std").reset_index(drop=True)


def get_stage_wins(event_id: int = _DEFAULT) -> pd.DataFrame:
    """
    Etapas ganadas por piloto (position == 1 en stage_times).

    Devuelve DataFrame con:
      entry_id, driver_name, manufacturer, win_count, stage_codes (lista)
    """
    times = loader.get_stage_times_enriched(event_id)
    if times.empty:
        return pd.DataFrame()

    winners = times[times["position"] == 1].copy()
    if winners.empty:
        return pd.DataFrame()

    # stage_code puede venir del CSV o necesitar merge
    if "stage_code" not in winners.columns:
        stages = loader.get_stages(event_id)[["stage_id", "stage_code"]]
        winners = winners.merge(stages, on="stage_id", how="left")

    group = winners.groupby(["entry_id", "driver_name", "manufacturer"])
    result = group.agg(
        win_count=("stage_code", "count"),
        stage_codes=("stage_code", lambda x: sorted(x.tolist())),
    ).reset_index()
    return result.sort_values("win_count", ascending=False).reset_index(drop=True)


def get_momentum(event_id: int = _DEFAULT) -> pd.DataFrame:
    """
    Momentum: diferencia de posicion entre primera y segunda mitad del rally.

    Positivo = mejora en la segunda mitad. Negativo = empeora.
    Requiere overall con evolucion por etapa (no solo clasificacion final).
    """
    df = loader.get_overall_enriched(event_id)
    if df.empty:
        return pd.DataFrame()

    stages = df["stage_id"].unique()
    if len(stages) < 2:
        logger.warning("Momentum requiere al menos 2 etapas (event_id=%d)", event_id)
        return pd.DataFrame()

    stages_sorted = sorted(stages)
    mid = len(stages_sorted) // 2
    first_half = stages_sorted[:mid]
    second_half = stages_sorted[mid:]

    result = []
    for entry_id, group in df.groupby("entry_id"):
        row0 = group.iloc[0]
        first = group[group["stage_id"].isin(first_half)]["position"].mean()
        second = group[group["stage_id"].isin(second_half)]["position"].mean()
        momentum = round(first - second, 2)  # positivo = mejora (posicion baja = mejor)
        result.append({
            "entry_id": int(entry_id),
            "driver_name": str(row0.get("driver_name", "")),
            "manufacturer": str(row0.get("manufacturer", "")),
            "avg_pos_first_half": round(float(first), 2) if not pd.isna(first) else None,
            "avg_pos_second_half": round(float(second), 2) if not pd.isna(second) else None,
            "momentum": momentum,
        })

    return pd.DataFrame(result).sort_values("momentum", ascending=False).reset_index(drop=True)
