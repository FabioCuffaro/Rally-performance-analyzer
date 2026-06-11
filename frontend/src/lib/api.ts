import type {
  DriverComparison,
  DriverEvolution,
  DriverPaceData,
  DriverSurfaceStats,
  EventSummary,
  MomentumEntry,
  OverallClassification,
  RallyStageWins,
  Stage,
  StageResult,
  Driver,
  ConsistencyIndex,
  SeasonStandings,
  DriverSeasonPace,
  SeasonSurfaceEntry,
  SeasonH2H,
} from '../types'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`)
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`)
  return res.json() as Promise<T>
}

export const api = {
  // ── Rallies ────────────────────────────────────────────────────────────────
  getRallies:        ()                                 => get<EventSummary[]>('/rallies/'),
  getRally:          (eventId: number)                  => get<EventSummary>(`/rallies/${eventId}`),
  getStageWins:      (eventId: number)                  => get<RallyStageWins>(`/rallies/${eventId}/stage-wins`),

  // ── Stages ─────────────────────────────────────────────────────────────────
  getStages:         (eventId: number)                  => get<Stage[]>(`/stages/?event_id=${eventId}`),
  getStageTimes:     (stageId: number, eventId: number) => get<StageResult>(`/stages/${stageId}/times?event_id=${eventId}`),

  // ── Drivers ────────────────────────────────────────────────────────────────
  getDrivers:           (eventId: number)               => get<Driver[]>(`/drivers/?event_id=${eventId}`),
  getClassification:    (eventId: number)               => get<OverallClassification>(`/drivers/classification?event_id=${eventId}`),
  getEvolution:         (eventId: number)               => get<DriverEvolution[]>(`/drivers/evolution?event_id=${eventId}`),
  compareDrivers:       (a: number, b: number, eventId: number) => get<DriverComparison>(`/drivers/compare?entry_a=${a}&entry_b=${b}&event_id=${eventId}`),
  getDriverPace:        (entryId: number, eventId: number)      => get<DriverPaceData>(`/drivers/${entryId}/pace?event_id=${eventId}`),
  getDriverConsistency: (entryId: number, eventId: number)      => get<ConsistencyIndex>(`/drivers/${entryId}/consistency?event_id=${eventId}`),
  getSurfaceStats:      (eventId: number)               => get<DriverSurfaceStats[]>(`/drivers/surface-stats?event_id=${eventId}`),
  getMomentum:          (eventId: number)               => get<MomentumEntry[]>(`/drivers/momentum?event_id=${eventId}`),

  // ── Season (V3) ────────────────────────────────────────────────────────────
  getSeasonStandings:      (eventIds: string)                              => get<SeasonStandings>(`/season/standings?event_ids=${eventIds}`),
  getSeasonPaceEvolution:  (eventIds: string)                              => get<DriverSeasonPace[]>(`/season/pace-evolution?event_ids=${eventIds}`),
  getSeasonSurfaceMastery: (eventIds: string)                              => get<SeasonSurfaceEntry[]>(`/season/surface-mastery?event_ids=${eventIds}`),
  getSeasonH2H:            (driverA: string, driverB: string, eventIds: string) =>
                             get<SeasonH2H>(`/season/h2h?driver_a=${encodeURIComponent(driverA)}&driver_b=${encodeURIComponent(driverB)}&event_ids=${eventIds}`),
}
