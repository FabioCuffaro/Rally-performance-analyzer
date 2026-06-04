"""Router de rally — endpoints de eventos y información general."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.models.schemas import EventSummary
from backend.app.services import data_loader as loader

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
    """Devuelve la información de un rally concreto."""
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
