"""Router de rally — endpoints de eventos e informacion general."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.models.schemas import EventSummary, RallyStageWins, StageWinEntry
from backend.app.services import analytics, data_loader as loader

router = APIRouter(prefix="/rallies", tags=["Rallies"])


@router.get("/", response_model=list[EventSummary])
def list_rallies() -> list[EventSummary]:
    """Devuelve todos los rallies de la temporada activa."""
    df = loader.get_events()
    if df.empty:
        return []
    return [
        EventSummary(
            event_id=int(row["event_id"]),
            name=str(row["name"]),
            status=str(row["status"]),
            country=str(row["country"]),
            country_iso=str(row.get("country_iso", "")),
            date_start=str(row.get("date_start", "")),
            date_finish=str(row.get("date_finish", "")),
        )
        for _, row in df.iterrows()
    ]


@router.get("/{event_id}", response_model=EventSummary)
def get_rally(event_id: int) -> EventSummary:
    """Devuelve la informacion de un rally concreto."""
    df = loader.get_events()
    row = df[df["event_id"] == event_id]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Rally {event_id} no encontrado")
    r = row.iloc[0]
    return EventSummary(
        event_id=int(r["event_id"]),
        name=str(r["name"]),
        status=str(r["status"]),
        country=str(r["country"]),
        country_iso=str(r.get("country_iso", "")),
        date_start=str(r.get("date_start", "")),
        date_finish=str(r.get("date_finish", "")),
    )


@router.get("/{event_id}/stage-wins", response_model=RallyStageWins)
def get_stage_wins(event_id: int) -> RallyStageWins:
    """Etapas ganadas por cada piloto en el rally."""
    # Verificar que el evento existe
    events_df = loader.get_events()
    if events_df[events_df["event_id"] == event_id].empty:
        # Tambien aceptar event_ids del registry aunque no esten en events.csv
        if event_id not in loader.RALLY_REGISTRY:
            raise HTTPException(status_code=404, detail=f"Rally {event_id} no encontrado")

    wins_df = analytics.get_stage_wins(event_id)
    if wins_df.empty:
        return RallyStageWins(event_id=event_id, wins=[])

    wins = [
        StageWinEntry(
            entry_id=int(r["entry_id"]),
            driver_name=str(r["driver_name"]),
            manufacturer=str(r["manufacturer"]),
            win_count=int(r["win_count"]),
            stage_codes=list(r["stage_codes"]),
        )
        for _, r in wins_df.iterrows()
    ]
    return RallyStageWins(event_id=event_id, wins=wins)
