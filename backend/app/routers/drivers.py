"""Router de pilotos — clasificación, evolución y comparativa."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from backend.app.models.schemas import (
    Driver,
    DriverComparison,
    DriverEvolution,
    DriverStageTime,
    OverallClassification,
    OverallEntry,
    PositionAtStage,
)
from backend.app.services import analytics, data_loader as loader
from backend.app.routers.stages import _isnan

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.get("/", response_model=list[Driver])
def list_drivers() -> list[Driver]:
    """Devuelve todos los pilotos inscritos en el rally."""
    df = loader.get_entries()
    if df.empty:
        return []
    return [
        Driver(
            entry_id=int(row["entry_id"]),
            driver_name=str(row["driver_name"]),
            driver_code=str(row.get("driver_code", "")),
            driver_nationality=str(row.get("driver_nationality", "")),
            codriver_name=str(row.get("codriver_name", "")),
            manufacturer=str(row.get("manufacturer", "")),
            car_number=str(row.get("car_number", "")),
            group=str(row.get("group", "")),
        )
        for _, row in df.iterrows()
    ]


@router.get("/classification", response_model=OverallClassification)
def get_final_classification() -> OverallClassification:
    """Devuelve la clasificación general final del rally."""
    df = analytics.get_final_classification()
    if df.empty:
        raise HTTPException(status_code=404, detail="No hay datos de clasificación")

    stages_df = loader.get_stages()
    last_stage_id = int(df.iloc[0]["stage_id"])
    stage_row = stages_df[stages_df["stage_id"] == last_stage_id]
    stage_code = str(stage_row.iloc[0]["stage_code"]) if not stage_row.empty else ""

    entries = [
        OverallEntry(
            entry_id=int(row["entry_id"]),
            position=int(row["position"]),
            total_time_s=float(row["total_time_s"]) if not _isnan(row.get("total_time_s")) else None,
            total_time_str=str(row.get("total_time_str", "")) or None,
            diff_first_s=float(row["diff_first_s"]) if not _isnan(row.get("diff_first_s")) else None,
            driver_name=str(row.get("driver_name", "")),
            driver_code=str(row.get("driver_code", "")),
            manufacturer=str(row.get("manufacturer", "")),
            car_number=str(row.get("car_number", "")),
        )
        for _, row in df.iterrows()
    ]

    return OverallClassification(
        event_id=int(df.iloc[0]["event_id"]),
        stage_id=last_stage_id,
        stage_code=stage_code,
        entries=entries,
    )


@router.get("/evolution", response_model=list[DriverEvolution])
def get_all_evolution() -> list[DriverEvolution]:
    """Devuelve la evolución de posición de todos los pilotos (bump chart)."""
    df = analytics.get_all_drivers_evolution()
    if df.empty:
        return []

    result = []
    for entry_id, group in df.groupby("entry_id"):
        row0 = group.iloc[0]
        positions = [
            PositionAtStage(
                stage_code=str(r.get("stage_code", "")),
                stage_id=int(r["stage_id"]),
                position=int(r["position"]),
                total_time_s=float(r["total_time_s"]) if not _isnan(r.get("total_time_s")) else None,
                diff_first_s=float(r["diff_first_s"]) if not _isnan(r.get("diff_first_s")) else None,
            )
            for _, r in group.iterrows()
        ]
        result.append(DriverEvolution(
            entry_id=int(entry_id),
            driver_name=str(row0.get("driver_name", "")),
            driver_code=str(row0.get("driver_code", "")),
            manufacturer=str(row0.get("manufacturer", "")),
            positions=positions,
        ))

    return result


@router.get("/compare", response_model=DriverComparison)
def compare_drivers(
    entry_a: int = Query(..., description="entry_id del piloto A"),
    entry_b: int = Query(..., description="entry_id del piloto B"),
) -> DriverComparison:
    """Compara los tiempos por etapa de dos pilotos."""
    entries_df = loader.get_entries()

    def _get_driver(entry_id: int) -> Driver:
        row = entries_df[entries_df["entry_id"] == entry_id]
        if row.empty:
            raise HTTPException(status_code=404, detail=f"Piloto {entry_id} no encontrado")
        r = row.iloc[0]
        return Driver(
            entry_id=int(r["entry_id"]),
            driver_name=str(r["driver_name"]),
            driver_code=str(r.get("driver_code", "")),
            driver_nationality=str(r.get("driver_nationality", "")),
            codriver_name=str(r.get("codriver_name", "")),
            manufacturer=str(r.get("manufacturer", "")),
            car_number=str(r.get("car_number", "")),
            group=str(r.get("group", "")),
        )

    driver_a = _get_driver(entry_a)
    driver_b = _get_driver(entry_b)

    data = analytics.get_driver_comparison(entry_a, entry_b)

    def _to_stage_times(df) -> list[DriverStageTime]:
        return [
            DriverStageTime(
                stage_code=str(r.get("stage_code", "")),
                position=int(r["position"]),
                time_s=float(r["time_s"]) if not _isnan(r.get("time_s")) else None,
                diff_first_s=float(r["diff_first_s"]) if not _isnan(r.get("diff_first_s")) else None,
            )
            for _, r in df.iterrows()
        ]

    return DriverComparison(
        event_id=1,
        driver_a=driver_a,
        driver_b=driver_b,
        stage_times_a=_to_stage_times(data["driver_a"]),
        stage_times_b=_to_stage_times(data["driver_b"]),
    )
