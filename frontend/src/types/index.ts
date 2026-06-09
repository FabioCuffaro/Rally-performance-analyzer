// ── Events ────────────────────────────────────────────────────────────────────

export interface EventSummary {
  event_id: number
  name: string
  status: string
  country: string
  country_iso: string
  date_start: string
  date_finish: string
}

// ── Stages ────────────────────────────────────────────────────────────────────

export interface Stage {
  stage_id: number
  stage_code: string
  name: string
  distance_km: number
  surface: string
  leg_name: string
  status: string
}

// ── Drivers ───────────────────────────────────────────────────────────────────

export interface Driver {
  entry_id: number
  driver_name: string
  driver_code: string
  driver_nationality: string
  codriver_name: string
  manufacturer: string
  car_number: string
  group: string
}

// ── Classification ────────────────────────────────────────────────────────────

export interface OverallEntry {
  entry_id: number
  position: number
  total_time_s: number | null
  total_time_str: string | null
  diff_first_s: number | null
  driver_name: string
  driver_code: string
  manufacturer: string
  car_number: string
}

export interface OverallClassification {
  event_id: number
  stage_id: number
  stage_code: string
  entries: OverallEntry[]
}

// ── Stage times ───────────────────────────────────────────────────────────────

export interface StageTimeEntry {
  entry_id: number
  position: number
  time_s: number | null
  time_str: string | null
  diff_first_s: number | null
  diff_prev_s: number | null
  status: string
  driver_name: string
  driver_code: string
  manufacturer: string
  car_number: string
}

export interface StageResult {
  event_id: number
  stage_id: number
  stage_code: string
  entries: StageTimeEntry[]
}

// ── Evolution ─────────────────────────────────────────────────────────────────

export interface PositionAtStage {
  stage_code: string
  stage_id: number
  position: number
  total_time_s: number | null
  diff_first_s: number | null
}

export interface DriverEvolution {
  entry_id: number
  driver_name: string
  driver_code: string
  manufacturer: string
  positions: PositionAtStage[]
}

// ── Comparison ────────────────────────────────────────────────────────────────

export interface DriverStageTime {
  stage_code: string
  position: number
  time_s: number | null
  diff_first_s: number | null
}

export interface DriverComparison {
  event_id: number
  driver_a: Driver
  driver_b: Driver
  stage_times_a: DriverStageTime[]
  stage_times_b: DriverStageTime[]
}

// ── V2 Metrics ────────────────────────────────────────────────────────────────

export interface StagePace {
  stage_code: string
  distance_km: number
  time_s: number
  pace_s_per_km: number
  surface: string
}

export interface DriverPaceData {
  entry_id: number
  driver_name: string
  manufacturer: string
  stages: StagePace[]
  avg_pace: number
}

export interface SurfaceStatEntry {
  surface: string
  avg_pace: number
  stage_count: number
}

export interface DriverSurfaceStats {
  entry_id: number
  driver_name: string
  manufacturer: string
  stats: SurfaceStatEntry[]
}

export interface ConsistencyIndex {
  entry_id: number
  driver_name: string
  manufacturer: string
  pace_mean: number
  pace_std: number
  stage_count: number
}

export interface StageWinEntry {
  entry_id: number
  driver_name: string
  manufacturer: string
  win_count: number
  stage_codes: string[]
}

export interface RallyStageWins {
  event_id: number
  wins: StageWinEntry[]
}

export interface MomentumEntry {
  entry_id: number
  driver_name: string
  manufacturer: string
  avg_pos_first_half: number | null
  avg_pos_second_half: number | null
  momentum: number
}
