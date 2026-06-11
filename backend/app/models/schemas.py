"""
Modelos Pydantic — esquemas de validacion y serializacion de la API.
V2: añadidos schemas para pace, surface stats, consistency, stage wins, momentum.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Eventos ───────────────────────────────────────────────────────────────────

class EventSummary(BaseModel):
    event_id: int
    name: str
    status: str
    country: str
    country_iso: str
    date_start: str
    date_finish: str


# ── Etapas ────────────────────────────────────────────────────────────────────

class Stage(BaseModel):
    stage_id: int
    stage_code: str
    name: str
    distance_km: float
    surface: str
    leg_name: str
    status: str


# ── Pilotos ───────────────────────────────────────────────────────────────────

class Driver(BaseModel):
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
    entry_id: int
    position: int
    time_s: float | None = None
    time_str: str | None = None
    diff_first_s: float | None = None
    diff_prev_s: float | None = None
    status: str
    driver_name: str = ""
    driver_code: str = ""
    manufacturer: str = ""
    car_number: str = ""


class StageResult(BaseModel):
    event_id: int
    stage_id: int
    stage_code: str
    entries: list[StageTimeEntry]


# ── Clasificacion general ─────────────────────────────────────────────────────

class OverallEntry(BaseModel):
    entry_id: int
    position: int
    total_time_s: float | None = None
    total_time_str: str | None = None
    diff_first_s: float | None = None
    driver_name: str = ""
    driver_code: str = ""
    manufacturer: str = ""
    car_number: str = ""


class OverallClassification(BaseModel):
    event_id: int
    stage_id: int
    stage_code: str
    entries: list[OverallEntry]


# ── Comparativa entre pilotos ─────────────────────────────────────────────────

class DriverStageTime(BaseModel):
    stage_code: str
    position: int
    time_s: float | None = None
    diff_first_s: float | None = None


class DriverComparison(BaseModel):
    event_id: int
    driver_a: Driver
    driver_b: Driver
    stage_times_a: list[DriverStageTime]
    stage_times_b: list[DriverStageTime]


# ── Evolucion de posiciones ───────────────────────────────────────────────────

class PositionAtStage(BaseModel):
    stage_code: str
    stage_id: int
    position: int
    total_time_s: float | None = None
    diff_first_s: float | None = None


class DriverEvolution(BaseModel):
    entry_id: int
    driver_name: str
    driver_code: str
    manufacturer: str
    positions: list[PositionAtStage]


# ── V2: Pace ──────────────────────────────────────────────────────────────────

class StagePace(BaseModel):
    """Pace de un piloto en una etapa concreta."""
    stage_code: str
    distance_km: float
    time_s: float
    pace_s_per_km: float
    surface: str


class DriverPaceData(BaseModel):
    """Pace de un piloto por etapa."""
    entry_id: int
    driver_name: str
    manufacturer: str
    stages: list[StagePace]
    avg_pace: float


# ── V2: Surface stats ─────────────────────────────────────────────────────────

class SurfaceStatEntry(BaseModel):
    """Stats de pace de un piloto en una superficie concreta."""
    surface: str
    avg_pace: float
    stage_count: int


class DriverSurfaceStats(BaseModel):
    """Rendimiento de un piloto por superficie."""
    entry_id: int
    driver_name: str
    manufacturer: str
    stats: list[SurfaceStatEntry]


# ── V2: Consistencia ──────────────────────────────────────────────────────────

class ConsistencyIndex(BaseModel):
    """Indice de consistencia de un piloto (std del pace)."""
    entry_id: int
    driver_name: str
    manufacturer: str
    pace_mean: float
    pace_std: float
    stage_count: int


# ── V2: Stage wins ────────────────────────────────────────────────────────────

class StageWinEntry(BaseModel):
    """Etapas ganadas por un piloto en el rally."""
    entry_id: int
    driver_name: str
    manufacturer: str
    win_count: int
    stage_codes: list[str]


class RallyStageWins(BaseModel):
    """Ganadores de etapa de un rally."""
    event_id: int
    wins: list[StageWinEntry]


# ── V2: Momentum ─────────────────────────────────────────────────────────────

class MomentumEntry(BaseModel):
    """Momentum de un piloto: mejora o empeora en la segunda mitad."""
    entry_id: int
    driver_name: str
    manufacturer: str
    avg_pos_first_half: float | None = None
    avg_pos_second_half: float | None = None
    momentum: float  # positivo = mejora, negativo = empeora

# ── V3: Season schemas ────────────────────────────────────────────────────────

class RallyPace(BaseModel):
    """Pace medio de un piloto en un rally."""
    event_id: int
    event_name: str
    avg_pace: float
    stage_count: int


class DriverSeasonPace(BaseModel):
    """Evolucion de pace de un piloto a lo largo de la temporada."""
    driver_name: str
    manufacturer: str
    paces: list[RallyPace]


class SeasonStandingsEntry(BaseModel):
    """Clasificacion de temporada de un piloto."""
    driver_name: str
    manufacturer: str
    total_points: int
    rally_points: dict[str, int]


class SeasonStandings(BaseModel):
    """Clasificacion completa de la temporada."""
    entries: list[SeasonStandingsEntry]
    event_ids: list[int]


class SeasonSurfaceEntry(BaseModel):
    """Pace de un piloto en una superficie a lo largo de la temporada."""
    driver_name: str
    manufacturer: str
    surface: str
    avg_pace: float
    stage_count: int
    rally_count: int


class SeasonH2HResult(BaseModel):
    """Resultado de un piloto en un rally del H2H."""
    event_id: int
    event_name: str
    position_a: int | None = None
    position_b: int | None = None
    points_a: int
    points_b: int
    winner: str


class SeasonH2H(BaseModel):
    """Comparativa H2H entre dos pilotos en la temporada."""
    driver_a: str
    driver_b: str
    results: list[SeasonH2HResult]
    wins_a: int
    wins_b: int
