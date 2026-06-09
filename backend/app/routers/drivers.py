"""Router de pilotos — clasificacion, evolucion, comparativa y metricas V2."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from backend.app.models.schemas import (
    ConsistencyIndex,
    Driver,
    DriverComparison,
    DriverEvolution,
    DriverPaceData,
    DriverStageTime,
    DriverSurfaceStats,
    MomentumEntry,
    OverallClassification,
    OverallEntry,
    PositionAtStage,
    StagePace,
    SurfaceStatEntry,
)
from backend.app.services import analytics, data_loader as loader
from backend.app.routers.stages import _isnan

router = APIRouter(prefix="/drivers", tags=["Drivers"])

_DEFAULT = loader.DEFAULT_EVENT_ID


# ── Endpoints existentes (ahora con ?event_id) ────────────────────────────────

@router.get("/", response_model=list[Driver])
def list_drivers(event_id: int = Query(_DEFAULT, description="ID del evento")) -> list[Driver]:
    df = loader.get_entries(event_id)
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
def get_final_classification(
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> OverallClassification:
    df = analytics.get_final_classification(event_id)
    if df.empty:
        raise HTTPException(status_code=404, detail="No hay datos de clasificacion")

    stages_df = loader.get_stages(event_id)
    last_stage_id = int(df.iloc[0]["stage_id"])

    stage_code = "FINAL"
    if not stages_df.empty and "stage_id" in stages_df.columns:
        stage_row = stages_df[stages_df["stage_id"] == last_stage_id]
        if not stage_row.empty:
            stage_code = str(stage_row.iloc[0]["stage_code"])

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
def get_all_evolution(
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> list[DriverEvolution]:
    df = analytics.get_all_drivers_evolution(event_id)
    if df.empty:
        return []

    result = []
    for eid, group in df.groupby("entry_id"):
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
            entry_id=int(eid),
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
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> DriverComparison:
    entries_df = loader.get_entries(event_id)

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
    data = analytics.get_driver_comparison(entry_a, entry_b, event_id)

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
        event_id=event_id,
        driver_a=driver_a,
        driver_b=driver_b,
        stage_times_a=_to_stage_times(data["driver_a"]),
        stage_times_b=_to_stage_times(data["driver_b"]),
    )


# ── Nuevos endpoints V2 ───────────────────────────────────────────────────────

@router.get("/{entry_id}/pace", response_model=DriverPaceData)
def get_driver_pace(
    entry_id: int,
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> DriverPaceData:
    """Pace por km del piloto en cada etapa."""
    pace_df = analytics.calculate_pace(event_id)
    if pace_df.empty:
        raise HTTPException(status_code=404, detail="Sin datos de pace para este evento")

    driver_df = pace_df[pace_df["entry_id"] == entry_id]
    if driver_df.empty:
        raise HTTPException(status_code=404, detail=f"Piloto {entry_id} sin datos de pace")

    row0 = driver_df.iloc[0]
    stages = [
        StagePace(
            stage_code=str(r["stage_code"]),
            distance_km=float(r["distance_km"]),
            time_s=float(r["time_s"]),
            pace_s_per_km=float(r["pace_s_per_km"]),
            surface=str(r.get("surface", "Tarmac")),
        )
        for _, r in driver_df.iterrows()
    ]
    avg_pace = round(float(driver_df["pace_s_per_km"].mean()), 3)

    return DriverPaceData(
        entry_id=entry_id,
        driver_name=str(row0.get("driver_name", "")),
        manufacturer=str(row0.get("manufacturer", "")),
        stages=stages,
        avg_pace=avg_pace,
    )


@router.get("/{entry_id}/consistency", response_model=ConsistencyIndex)
def get_driver_consistency(
    entry_id: int,
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> ConsistencyIndex:
    """Indice de consistencia del piloto (std del pace entre etapas)."""
    consistency_df = analytics.calculate_consistency(event_id)
    if consistency_df.empty:
        raise HTTPException(status_code=404, detail="Sin datos de consistencia para este evento")

    row = consistency_df[consistency_df["entry_id"] == entry_id]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Piloto {entry_id} sin datos de consistencia")

    r = row.iloc[0]
    return ConsistencyIndex(
        entry_id=entry_id,
        driver_name=str(r.get("driver_name", "")),
        manufacturer=str(r.get("manufacturer", "")),
        pace_mean=float(r["pace_mean"]),
        pace_std=float(r["pace_std"]),
        stage_count=int(r["stage_count"]),
    )


@router.get("/surface-stats", response_model=list[DriverSurfaceStats])
def get_surface_stats(
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> list[DriverSurfaceStats]:
    """Rendimiento de todos los pilotos por superficie."""
    surface_df = analytics.get_surface_analysis(event_id)
    if surface_df.empty:
        return []

    result = []
    for eid, group in surface_df.groupby("entry_id"):
        row0 = group.iloc[0]
        stats = [
            SurfaceStatEntry(
                surface=str(r["surface"]),
                avg_pace=float(r["avg_pace"]),
                stage_count=int(r["stage_count"]),
            )
            for _, r in group.iterrows()
        ]
        result.append(DriverSurfaceStats(
            entry_id=int(eid),
            driver_name=str(row0.get("driver_name", "")),
            manufacturer=str(row0.get("manufacturer", "")),
            stats=stats,
        ))
    return result


@router.get("/momentum", response_model=list[MomentumEntry])
def get_momentum(
    event_id: int = Query(_DEFAULT, description="ID del evento"),
) -> list[MomentumEntry]:
    """Momentum de todos los pilotos (mejora/empeora en segunda mitad del rally)."""
    df = analytics.get_momentum(event_id)
    if df.empty:
        return []
    return [
        MomentumEntry(
            entry_id=int(r["entry_id"]),
            driver_name=str(r["driver_name"]),
            manufacturer=str(r["manufacturer"]),
            avg_pos_first_half=float(r["avg_pos_first_half"]) if r["avg_pos_first_half"] else None,
            avg_pos_second_half=float(r["avg_pos_second_half"]) if r["avg_pos_second_half"] else None,
            momentum=float(r["momentum"]),
        )
        for _, r in df.iterrows()
    ]
