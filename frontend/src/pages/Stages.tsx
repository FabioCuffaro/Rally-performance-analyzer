import { useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import { useRally } from '../context/RallyContext'
import { useApi } from '../hooks/useApi'
import { api } from '../lib/api'
import { LoadingSpinner, ErrorMessage } from '../components/ui/LoadingSpinner'
import type { StageTimeEntry } from '../types'

const MFR_COLORS: Record<string, string> = {
  Toyota:    '#ef4444',
  Hyundai:   '#3b82f6',
  Ford:      '#06b6d4',
  'M-Sport': '#06b6d4',
}
const DEFAULT_COLOR = '#71717a'

function mfrColor(mfr: string) {
  return MFR_COLORS[mfr] ?? DEFAULT_COLOR
}

function fmtGap(diff: number | null, pos: number) {
  if (pos === 1 || diff === null || diff === 0) return '—'
  return `+${diff.toFixed(1)}s`
}

function posBadge(pos: number) {
  const base = 'inline-flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold'
  if (pos === 1) return `${base} bg-rally-gold text-black`
  if (pos === 2) return `${base} bg-rally-silver text-black`
  if (pos === 3) return `${base} bg-rally-bronze text-white`
  return `${base} bg-surface-hover text-zinc-400`
}

const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null
  const d = payload[0].payload as StageTimeEntry & { gap_s: number }
  return (
    <div className="rounded-lg border border-surface-border bg-surface-card px-3 py-2 text-xs shadow-xl">
      <p className="font-bold text-white">P{d.position} — {d.driver_name}</p>
      <p className="text-zinc-400">{d.manufacturer} #{d.car_number}</p>
      <p className="mt-1 text-rally-red font-mono">{d.time_str}</p>
      {d.position > 1 && <p className="text-zinc-500 font-mono">+{d.diff_first_s?.toFixed(1)}s</p>}
    </div>
  )
}

export function Stages() {
  const { eventId } = useRally()
  const [selectedStageId, setSelectedStageId] = useState<number | null>(null)

  const { data: stages, loading: loadingStages } = useApi(
    () => api.getStages(eventId),
    [eventId],
  )

  const stageId = selectedStageId ?? stages?.[0]?.stage_id ?? null

  const { data: stageResult, loading: loadingTimes, error } = useApi(
    () => (stageId ? api.getStageTimes(stageId, eventId) : Promise.resolve(null)),
    [stageId, eventId],
  )

  const chartData = stageResult?.entries ?? []

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Stage Times</h1>
        <p className="mt-1 text-sm text-zinc-500">Tiempos y posiciones por etapa</p>
      </div>

      {/* Stage selector */}
      {loadingStages ? (
        <LoadingSpinner size="sm" />
      ) : (
        <div className="flex flex-wrap gap-2">
          {stages?.map(s => (
            <button
              key={s.stage_id}
              onClick={() => setSelectedStageId(s.stage_id)}
              className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                (selectedStageId ?? stages[0]?.stage_id) === s.stage_id
                  ? 'bg-rally-red text-white'
                  : 'bg-surface-card border border-surface-border text-zinc-400 hover:border-zinc-500 hover:text-white'
              }`}
            >
              {s.stage_code}
              <span className="ml-1 text-xs opacity-60">{s.distance_km}km</span>
            </button>
          ))}
        </div>
      )}

      {loadingTimes && <LoadingSpinner />}
      {error && (
        <ErrorMessage message="Sin datos de tiempos para esta etapa en este rally." />
      )}

      {!loadingTimes && !error && chartData.length > 0 && (
        <>
          {/* Stage info */}
          {stageResult && (
            <div className="text-sm text-zinc-500">
              <span className="font-medium text-white">{stageResult.stage_code}</span>
              {' · '}
              {chartData.length} pilotos
            </div>
          )}

          {/* Bar chart */}
          <div className="card p-4">
            <h2 className="mb-4 text-xs font-semibold uppercase tracking-wider text-zinc-500">
              Tiempo por piloto (s)
            </h2>
            <ResponsiveContainer width="100%" height={Math.max(200, chartData.length * 36)}>
              <BarChart
                data={chartData}
                layout="vertical"
                margin={{ left: 8, right: 32, top: 4, bottom: 4 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                <XAxis
                  type="number"
                  domain={['dataMin - 5', 'dataMax + 5']}
                  tick={{ fill: '#71717a', fontSize: 11 }}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  type="category"
                  dataKey="driver_name"
                  width={100}
                  tick={{ fill: '#a1a1aa', fontSize: 11 }}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
                <Bar dataKey="time_s" radius={[0, 4, 4, 0]}>
                  {chartData.map((entry, i) => (
                    <Cell key={i} fill={mfrColor(entry.manufacturer)} fillOpacity={0.85} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Table */}
          <div className="card overflow-hidden p-0">
            <div className="border-b border-surface-border px-5 py-3">
              <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
                Clasificacion de etapa
              </h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-surface-border text-xs font-medium uppercase tracking-wider text-zinc-500">
                    <th className="px-4 py-3 text-left">Pos</th>
                    <th className="px-4 py-3 text-left">No.</th>
                    <th className="px-4 py-3 text-left">Piloto</th>
                    <th className="px-4 py-3 text-left">Fabricante</th>
                    <th className="px-4 py-3 text-right">Tiempo</th>
                    <th className="px-4 py-3 text-right">Gap</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-surface-border">
                  {chartData.map(entry => (
                    <tr key={entry.entry_id} className="hover:bg-surface-hover/50 transition-colors">
                      <td className="px-4 py-2.5">
                        <span className={posBadge(entry.position)}>{entry.position}</span>
                      </td>
                      <td className="px-4 py-2.5 font-mono text-xs text-zinc-500">#{entry.car_number}</td>
                      <td className="px-4 py-2.5 font-medium text-white">{entry.driver_name}</td>
                      <td className="px-4 py-2.5 text-sm" style={{ color: mfrColor(entry.manufacturer) }}>
                        {entry.manufacturer}
                      </td>
                      <td className="px-4 py-2.5 text-right font-mono text-zinc-300">{entry.time_str ?? '—'}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-zinc-500">
                        {fmtGap(entry.diff_first_s, entry.position)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
