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
} from '../types'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`)
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${path}`)
  }
  return res.json() as Promise<T>
}

export const api = {
  // ── Rallies ────────────────────────────────────────────────────────────────
  getRallies: () =>
    get<EventSummary[]>('/rallies/'),

  getRally: (eventId: number) =>
    get<EventSummary>(`/rallies/${eventId}`),

  getStageWins: (eventId: number) =>
    get<RallyStageWins>(`/rallies/${eventId}/stage-wins`),

  // ── Stages ─────────────────────────────────────────────────────────────────
  getStages: (eventId: number) =>
    get<Stage[]>(`/stages/?event_id=${eventId}`),

  getStageTimes: (stageId: number) =>
    get<StageResult>(`/stages/${stageId}/times`),

  // ── Drivers ────────────────────────────────────────────────────────────────
  getDrivers: (eventId: number) =>
    get<Driver[]>(`/drivers/?event_id=${eventId}`),

  getClassification: (eventId: number) =>
    get<OverallClassification>(`/drivers/classification?event_id=${eventId}`),

  getEvolution: (eventId: number) =>
    get<DriverEvolution[]>(`/drivers/evolution?event_id=${eventId}`),

  compareDrivers: (entryA: number, entryB: number, eventId: number) =>
    get<DriverComparison>(`/drivers/compare?entry_a=${entryA}&entry_b=${entryB}&event_id=${eventId}`),

  // ── V2 Metrics ─────────────────────────────────────────────────────────────
  getDriverPace: (entryId: number, eventId: number) =>
    get<DriverPaceData>(`/drivers/${entryId}/pace?event_id=${eventId}`),

  getDriverConsistency: (entryId: number, eventId: number) =>
    get<ConsistencyIndex>(`/drivers/${entryId}/consistency?event_id=${eventId}`),

  getSurfaceStats: (eventId: number) =>
    get<DriverSurfaceStats[]>(`/drivers/surface-stats?event_id=${eventId}`),

  getMomentum: (eventId: number) =>
    get<MomentumEntry[]>(`/drivers/momentum?event_id=${eventId}`),
}
