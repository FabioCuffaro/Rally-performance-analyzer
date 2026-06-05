"""
Servicio de analitica.

Funciones de calculo y transformacion sobre los DataFrames cargados.
"""

from __future__ import annotations

import logging

import pandas as pd

from backend.app.services import data_loader as loader

logger = logging.getLogger(__name__)


def get_stage_result(stage_id: int) -> pd.DataFrame:
    """Tiempos enriquecidos de una etapa concreta, ordenados por posicion."""
    df = loader.get_stage_times_enriched()
    if df.empty:
        return df
    result = df[df["stage_id"] == stage_id].sort_values("position")
    return result.reset_index(drop=True)


def get_overall_at_stage(stage_id: int) -> pd.DataFrame:
    """Clasificacion general enriquecida tras una etapa concreta."""
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    result = df[df["stage_id"] == stage_id].sort_values("position")
    return result.reset_index(drop=True)


def get_final_classification() -> pd.DataFrame:
    """Clasificacion final del rally (tras la ultima etapa)."""
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    last_stage = df["stage_id"].max()
    return get_overall_at_stage(last_stage)


def get_driver_evolution(entry_id: int) -> pd.DataFrame:
    """Evolucion de posicion de un piloto etapa a etapa."""
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    # stage_code ya existe en el CSV — no hace falta merge adicional
    result = df[df["entry_id"] == entry_id].copy()
    return result.sort_values("stage_id").reset_index(drop=True)


def get_all_drivers_evolution() -> pd.DataFrame:
    """Evolucion de posicion de todos los pilotos (bump chart)."""
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    # stage_code ya existe en el CSV — no hace falta merge adicional
    # Solo aseguramos que la columna existe; si no, usamos stage_id como fallback
    if "stage_code" not in df.columns:
        stages = loader.get_stages()[["stage_id", "stage_code"]].copy()
        df = df.merge(stages, on="stage_id", how="left")
    return df.sort_values(["entry_id", "stage_id"]).reset_index(drop=True)


def get_driver_comparison(entry_id_a: int, entry_id_b: int) -> dict:
    """Tiempos por etapa de dos pilotos para comparativa."""
    times = loader.get_stage_times_enriched()

    def _get_driver_times(entry_id: int) -> pd.DataFrame:
        df = times[times["entry_id"] == entry_id].copy()
        # stage_code ya existe en el CSV — no hace falta merge adicional
        if "stage_code" not in df.columns:
            stages = loader.get_stages()[["stage_id", "stage_code"]]
            df = df.merge(stages, on="stage_id", how="left")
        return df.sort_values("stage_id").reset_index(drop=True)

    return {
        "driver_a": _get_driver_times(entry_id_a),
        "driver_b": _get_driver_times(entry_id_b),
    }
