"""Router de etapas — endpoints de etapas y tiempos."""

from __future__ import annotations
import math

from fastapi import APIRouter, HTTPException, Query

from backend.app.models.schemas import Stage, StageResult, StageTimeEntry
from backend.app.services import analytics, data_loader as loader

router = APIRouter(prefix="/stages", tags=["Stages"])

_DEFAULT = loader.DEFAULT_EVENT_ID


@router.get("/", response_model=list[Stage])
def list_stages(
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> list[Stage]:
    """Devuelve todas las etapas del rally."""
    df = loader.get_stages(event_id)
    if df.empty:
        return []
    return [
        Stage(
            stage_id=int(row["stage_id"]),
            stage_code=str(row["stage_code"]),
            name=str(row["name"]),
            distance_km=float(row["distance_km"]),
            surface=str(row["surface"]),
            leg_name=str(row.get("leg_name", "")),
            status=str(row.get("status", "")),
        )
        for _, row in df.iterrows()
    ]


@router.get("/{stage_id}/times", response_model=StageResult)
def get_stage_times(
    stage_id: int,
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> StageResult:
    """Devuelve los tiempos de todos los pilotos en una etapa concreta."""
    stages_df = loader.get_stages(event_id)

    if stages_df.empty or "stage_id" not in stages_df.columns:
        raise HTTPException(status_code=404, detail=f"Etapa {stage_id} no encontrada")

    stage_row = stages_df[stages_df["stage_id"] == stage_id]
    if stage_row.empty:
        raise HTTPException(status_code=404, detail=f"Etapa {stage_id} no encontrada")

    stage_code = str(stage_row.iloc[0]["stage_code"])
    df = analytics.get_stage_result(stage_id, event_id)

    entries = [
        StageTimeEntry(
            entry_id=int(row["entry_id"]),
            position=int(row["position"]),
            time_s=float(row["time_s"]) if not _isnan(row.get("time_s")) else None,
            time_str=str(row["time_str"]) if row.get("time_str") else None,
            diff_first_s=float(row["diff_first_s"]) if not _isnan(row.get("diff_first_s")) else None,
            diff_prev_s=float(row["diff_prev_s"]) if not _isnan(row.get("diff_prev_s")) else None,
            status=str(row.get("status", "")),
            driver_name=str(row.get("driver_name", "")),
            driver_code=str(row.get("driver_code", "")),
            manufacturer=str(row.get("manufacturer", "")),
            car_number=str(row.get("car_number", "")),
        )
        for _, row in df.iterrows()
    ]

    return StageResult(
        event_id=int(df.iloc[0]["event_id"]) if not df.empty else 0,
        stage_id=stage_id,
        stage_code=stage_code,
        entries=entries,
    )


def _isnan(val) -> bool:
    try:
        return math.isnan(float(val))
    except (TypeError, ValueError):
        return val is None
