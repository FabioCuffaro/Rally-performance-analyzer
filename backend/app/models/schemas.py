"""
Modelos Pydantic — esquemas de validación y serialización de la API.

Cada schema representa la estructura de datos que devuelven los endpoints.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Eventos ───────────────────────────────────────────────────────────────────

class EventSummary(BaseModel):
    """Resumen de un evento/rally."""
    event_id: int
    name: str
    status: str
    country: str
    country_iso: str
    date_start: str
    date_finish: str


# ── Etapas ────────────────────────────────────────────────────────────────────

class Stage(BaseModel):
    """Información de una etapa."""
    stage_id: int
    stage_code: str
    name: str
    distance_km: float
    surface: str
    leg_name: str
    status: str


# ── Pilotos ───────────────────────────────────────────────────────────────────

class Driver(BaseModel):
    """Información de un piloto inscrito."""
    entry_id: int
    driver_name: str
    driver_code: str
    driver_nationality: str
    codriver_name: str
    manufacturer: str
    car_number: str
    group: str


# ── Tiempos de etapa ──────────────────────────────────────────────────────────

class StageTimeEntry(BaseModel):
    """Tiempo de un piloto en una etapa concreta."""
    entry_id: int
    position: int
    time_s: float | None = None
    time_str: str | None = None
    diff_first_s: float | None = None
    diff_prev_s: float | None = None
    status: str
    # Enriquecido con datos del piloto
    driver_name: str = ""
    driver_code: str = ""
    manufacturer: str = ""
    car_number: str = ""


class StageResult(BaseModel):
    """Resultado completo de una etapa."""
    event_id: int
    stage_id: int
    stage_code: str
    entries: list[StageTimeEntry]


# ── Clasificación general ─────────────────────────────────────────────────────

class OverallEntry(BaseModel):
    """Posición de un piloto en la clasificación general."""
    entry_id: int
    position: int
    total_time_s: float | None = None
    total_time_str: str | None = None
    diff_first_s: float | None = None
    # Enriquecido
    driver_name: str = ""
    driver_code: str = ""
    manufacturer: str = ""
    car_number: str = ""


class OverallClassification(BaseModel):
    """Clasificación general tras una etapa."""
    event_id: int
    stage_id: int
    stage_code: str
    entries: list[OverallEntry]


# ── Comparativa entre pilotos ─────────────────────────────────────────────────

class DriverStageTime(BaseModel):
    """Tiempo de un piloto en una etapa para comparativa."""
    stage_code: str
    position: int
    time_s: float | None = None
    diff_first_s: float | None = None


class DriverComparison(BaseModel):
    """Comparativa de dos pilotos a lo largo del rally."""
    event_id: int
    driver_a: Driver
    driver_b: Driver
    stage_times_a: list[DriverStageTime]
    stage_times_b: list[DriverStageTime]


# ── Evolución de posiciones ───────────────────────────────────────────────────

class PositionAtStage(BaseModel):
    """Posición de un piloto tras cada etapa."""
    stage_code: str
    stage_id: int
    position: int
    total_time_s: float | None = None
    diff_first_s: float | None = None


class DriverEvolution(BaseModel):
    """Evolución de posición de un piloto a lo largo del rally."""
    entry_id: int
    driver_name: str
    driver_code: str
    manufacturer: str
    positions: list[PositionAtStage]
