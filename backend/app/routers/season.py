"""Router de temporada — endpoints de analisis cross-rally."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from backend.app.models.schemas import (
    SeasonStandings,
    SeasonStandingsEntry,
    DriverSeasonPace,
    RallyPace,
    SeasonSurfaceEntry,
    SeasonH2H,
    SeasonH2HResult,
)
from backend.app.services import season_analytics as sa
from backend.app.services.data_loader import RALLY_REGISTRY

router = APIRouter(prefix="/season", tags=["Season"])

_DEFAULT_IDS = "89918,90090"


def _parse_ids(event_ids: str) -> list[int]:
    try:
        ids = [int(x.strip()) for x in event_ids.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=422, detail="event_ids debe ser lista separada por comas")
    valid = [i for i in ids if i in RALLY_REGISTRY]
    if not valid:
        raise HTTPException(status_code=404, detail="Ningun event_id valido encontrado")
    return valid


@router.get("/standings", response_model=SeasonStandings)
def get_standings(
    event_ids: str = Query(_DEFAULT_IDS, description="IDs de eventos separados por coma"),
) -> SeasonStandings:
    """Puntos FIA acumulados por piloto en la temporada."""
    ids = _parse_ids(event_ids)
    df = sa.get_season_standings(ids)
    if df.empty:
        return SeasonStandings(entries=[], event_ids=ids)

    pts_cols = {c: c.replace("points_", "") for c in df.columns if c.startswith("points_")}

    entries = []
    for _, row in df.iterrows():
        rally_pts = {pts_cols[c]: int(row[c]) for c in pts_cols}
        entries.append(SeasonStandingsEntry(
            driver_name=str(row["driver_name"]),
            manufacturer=str(row["manufacturer"]),
            total_points=int(row["total_points"]),
            rally_points=rally_pts,
        ))

    return SeasonStandings(entries=entries, event_ids=ids)


@router.get("/pace-evolution", response_model=list[DriverSeasonPace])
def get_pace_evolution(
    event_ids: str = Query(_DEFAULT_IDS, description="IDs de eventos separados por coma"),
) -> list[DriverSeasonPace]:
    """Pace medio por piloto y rally."""
    ids = _parse_ids(event_ids)
    df = sa.get_season_pace_evolution(ids)
    if df.empty:
        return []

    result = []
    for (driver_name, manufacturer), group in df.groupby(["driver_name", "manufacturer"]):
        paces = [
            RallyPace(
                event_id=int(r["event_id"]),
                event_name=str(r["event_name"]),
                avg_pace=float(r["avg_pace"]),
                stage_count=int(r["stage_count"]),
            )
            for _, r in group.sort_values("event_id").iterrows()
        ]
        result.append(DriverSeasonPace(
            driver_name=str(driver_name),
            manufacturer=str(manufacturer),
            paces=paces,
        ))

    return sorted(result, key=lambda x: x.paces[0].avg_pace if x.paces else 999)


@router.get("/surface-mastery", response_model=list[SeasonSurfaceEntry])
def get_surface_mastery(
    event_ids: str = Query(_DEFAULT_IDS, description="IDs de eventos separados por coma"),
) -> list[SeasonSurfaceEntry]:
    """Pace por superficie acumulado en la temporada."""
    ids = _parse_ids(event_ids)
    df = sa.get_season_surface_mastery(ids)
    if df.empty:
        return []

    return [
        SeasonSurfaceEntry(
            driver_name=str(r["driver_name"]),
            manufacturer=str(r["manufacturer"]),
            surface=str(r["surface"]),
            avg_pace=float(r["avg_pace"]),
            stage_count=int(r["stage_count"]),
            rally_count=int(r["rally_count"]),
        )
        for _, r in df.iterrows()
    ]


@router.get("/h2h", response_model=SeasonH2H)
def get_h2h(
    driver_a: str = Query(..., description="Nombre exacto del piloto A"),
    driver_b: str = Query(..., description="Nombre exacto del piloto B"),
    event_ids: str = Query(_DEFAULT_IDS, description="IDs de eventos separados por coma"),
) -> SeasonH2H:
    """Comparativa entre dos pilotos a lo largo de la temporada."""
    ids = _parse_ids(event_ids)
    df = sa.get_season_h2h(driver_a, driver_b, ids)
    if df.empty:
        raise HTTPException(status_code=404, detail="Sin datos para estos pilotos en los rallies seleccionados")

    results = [
        SeasonH2HResult(
            event_id=int(r["event_id"]),
            event_name=str(r["event_name"]),
            position_a=int(r["position_a"]) if r["position_a"] is not None else None,
            position_b=int(r["position_b"]) if r["position_b"] is not None else None,
            points_a=int(r["points_a"]),
            points_b=int(r["points_b"]),
            winner=str(r["winner"]),
        )
        for _, r in df.iterrows()
    ]

    wins_a = sum(1 for r in results if r.winner == "A")
    wins_b = sum(1 for r in results if r.winner == "B")

    return SeasonH2H(
        driver_a=driver_a,
        driver_b=driver_b,
        results=results,
        wins_a=wins_a,
        wins_b=wins_b,
    )
