"""
Servicio de analítica.

Funciones de cálculo y transformación sobre los DataFrames cargados.
Separa la lógica de negocio de los routers.
"""

from __future__ import annotations

import logging

import pandas as pd

from backend.app.services import data_loader as loader

logger = logging.getLogger(__name__)


def get_stage_result(stage_id: int) -> pd.DataFrame:
    """
    Devuelve los tiempos enriquecidos de una etapa concreta, ordenados por posición.
    """
    df = loader.get_stage_times_enriched()
    if df.empty:
        return df
    result = df[df["stage_id"] == stage_id].sort_values("position")
    return result.reset_index(drop=True)


def get_overall_at_stage(stage_id: int) -> pd.DataFrame:
    """
    Devuelve la clasificación general enriquecida tras una etapa concreta.
    """
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    result = df[df["stage_id"] == stage_id].sort_values("position")
    return result.reset_index(drop=True)


def get_final_classification() -> pd.DataFrame:
    """
    Devuelve la clasificación final del rally (tras la última etapa).
    """
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    last_stage = df["stage_id"].max()
    return get_overall_at_stage(last_stage)


def get_driver_evolution(entry_id: int) -> pd.DataFrame:
    """
    Devuelve la evolución de posición de un piloto etapa a etapa.
    """
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    stages = loader.get_stages()[["stage_id", "stage_code"]].copy()
    result = df[df["entry_id"] == entry_id].copy()
    result = result.merge(stages, on="stage_id", how="left")
    return result.sort_values("stage_id").reset_index(drop=True)


def get_all_drivers_evolution() -> pd.DataFrame:
    """
    Devuelve la evolución de posición de todos los pilotos (para el bump chart).
    """
    df = loader.get_overall_enriched()
    if df.empty:
        return df
    stages = loader.get_stages()[["stage_id", "stage_code"]].copy()
    result = df.merge(stages, on="stage_id", how="left")
    return result.sort_values(["entry_id", "stage_id"]).reset_index(drop=True)


def get_driver_comparison(entry_id_a: int, entry_id_b: int) -> dict:
    """
    Devuelve los tiempos por etapa de dos pilotos para comparativa.
    """
    times = loader.get_stage_times_enriched()
    stages = loader.get_stages()[["stage_id", "stage_code"]]

    def _get_driver_times(entry_id: int) -> pd.DataFrame:
        df = times[times["entry_id"] == entry_id].copy()
        df = df.merge(stages, on="stage_id", how="left")
        return df.sort_values("stage_id").reset_index(drop=True)

    return {
        "driver_a": _get_driver_times(entry_id_a),
        "driver_b": _get_driver_times(entry_id_b),
    }
