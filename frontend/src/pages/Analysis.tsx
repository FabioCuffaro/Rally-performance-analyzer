import { useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import { useRally } from '../context/RallyContext'
import { useApi } from '../hooks/useApi'
import { api } from '../lib/api'
import { LoadingSpinner, ErrorMessage } from '../components/ui/LoadingSpinner'

const SURFACE_COLORS: Record<string, string> = {
  Tarmac: '#f59e0b',
  Snow:   '#93c5fd',
  Gravel: '#a3e635',
  Ice:    '#67e8f9',
}

const PaceTooltip = ({ active, payload }: any) => {
  if (!active || !payload?.length) return null
  const d = payload[0].payload
  return (
    <div className="rounded-lg border border-surface-border bg-surface-card px-3 py-2 text-xs shadow-xl">
      <p className="font-bold text-white">{d.stage_code}</p>
      <p className="text-zinc-400">{d.surface} · {d.distance_km}km</p>
      <p className="mt-1 font-mono text-rally-red">{d.pace_s_per_km?.toFixed(2)} s/km</p>
      <p className="font-mono text-zinc-500">{d.time_s?.toFixed(1)}s total</p>
    </div>
  )
}

export function Analysis() {
  const { eventId } = useRally()
  const [selectedEntryId, setSelectedEntryId] = useState<number | null>(null)

  const { data: drivers } = useApi(() => api.getDrivers(eventId), [eventId])
  const { data: stageWins, loading: loadingWins } = useApi(() => api.getStageWins(eventId), [eventId])

  const entryId = selectedEntryId ?? drivers?.[0]?.entry_id ?? null

  const {
    data: paceData,
    loading: loadingPace,
    error: paceError,
  } = useApi(
    () => (entryId ? api.getDriverPace(entryId, eventId) : Promise.resolve(null)),
    [entryId, eventId],
  )

  const { data: surfaceStats } = useApi(() => api.getSurfaceStats(eventId), [eventId])

  // Build consistency table from surface stats
  const consistencyData = surfaceStats
    ? surfaceStats
        .map(d => ({
          entry_id: d.entry_id,
          driver_name: d.driver_name,
          manufacturer: d.manufacturer,
          avg_pace: d.stats.reduce((sum, s) => sum + s.avg_pace, 0) / d.stats.length,
        }))
        .sort((a, b) => a.avg_pace - b.avg_pace)
        .slice(0, 15)
    : []

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white">Pace & Analysis</h1>
        <p className="mt-1 text-sm text-zinc-500">Metricas avanzadas: pace, consistencia y etapas ganadas</p>
      </div>

      {/* ── Pace section ───────────────────────────────────────────────────── */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-semibold text-white">Pace por etapa</h2>
          <select
            value={entryId ?? ''}
            onChange={e => setSelectedEntryId(Number(e.target.value))}
            className="rounded-lg border border-surface-border bg-surface-hover px-3 py-1.5 text-sm text-white focus:border-rally-red focus:outline-none"
          >
            {drivers?.map(d => (
              <option key={d.entry_id} value={d.entry_id}>
                #{d.car_number} {d.driver_name}
              </option>
            ))}
          </select>
        </div>

        {loadingPace && <LoadingSpinner size="sm" />}
        {paceError && (
          <ErrorMessage message="Sin datos de pace para este rally. Selecciona un rally con tiempos por etapa." />
        )}

        {paceData && paceData.stages.length > 0 && (
          <>
            {/* Driver summary */}
            <div className="grid grid-cols-3 gap-4">
              <div className="card p-4">
                <div className="text-xs text-zinc-500 uppercase tracking-wider">Piloto</div>
                <div className="mt-1 font-bold text-white">{paceData.driver_name}</div>
                <div className="text-xs text-zinc-500">{paceData.manufacturer}</div>
              </div>
              <div className="card p-4">
                <div className="text-xs text-zinc-500 uppercase tracking-wider">Pace medio</div>
                <div className="mt-1 text-xl font-bold text-rally-red">{paceData.avg_pace.toFixed(2)}</div>
                <div className="text-xs text-zinc-500">s/km</div>
              </div>
              <div className="card p-4">
                <div className="text-xs text-zinc-500 uppercase tracking-wider">Etapas</div>
                <div className="mt-1 text-xl font-bold text-white">{paceData.stages.length}</div>
              </div>
            </div>

            {/* Pace bar chart */}
            <div className="card p-4">
              <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-zinc-500">
                Pace (s/km) por etapa — coloreado por superficie
              </h3>
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={paceData.stages} margin={{ left: 0, right: 16, top: 4, bottom: 4 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                  <XAxis dataKey="stage_code" tick={{ fill: '#71717a', fontSize: 12 }} tickLine={false} axisLine={{ stroke: '#27272a' }} />
                  <YAxis
                    domain={['dataMin - 2', 'dataMax + 2']}
                    tick={{ fill: '#71717a', fontSize: 11 }}
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={v => `${v}s`}
                  />
                  <Tooltip content={<PaceTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
                  <Bar dataKey="pace_s_per_km" radius={[4, 4, 0, 0]}>
                    {paceData.stages.map((s, i) => (
                      <Cell
                        key={i}
                        fill={SURFACE_COLORS[s.surface] ?? '#ef4444'}
                        fillOpacity={0.85}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              {/* Surface legend */}
              <div className="mt-3 flex flex-wrap gap-3">
                {Object.entries(SURFACE_COLORS).map(([surface, color]) => (
                  <div key={surface} className="flex items-center gap-1.5 text-xs text-zinc-500">
                    <span className="h-2.5 w-2.5 rounded-sm" style={{ backgroundColor: color }} />
                    {surface}
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </section>

      {/* ── Pace ranking ───────────────────────────────────────────────────── */}
      {consistencyData.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-base font-semibold text-white">Ranking por pace medio</h2>
          <div className="card overflow-hidden p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-surface-border text-xs text-zinc-500 uppercase tracking-wider">
                    <th className="px-4 py-3 text-left">Rank</th>
                    <th className="px-4 py-3 text-left">Piloto</th>
                    <th className="px-4 py-3 text-left">Fabricante</th>
                    <th className="px-4 py-3 text-right">Pace medio (s/km)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-surface-border">
                  {consistencyData.map((d, i) => (
                    <tr key={d.entry_id} className="hover:bg-surface-hover/50 transition-colors">
                      <td className="px-4 py-2.5 font-bold text-zinc-400">#{i + 1}</td>
                      <td className="px-4 py-2.5 font-medium text-white">{d.driver_name}</td>
                      <td className="px-4 py-2.5 text-zinc-400">{d.manufacturer}</td>
                      <td className="px-4 py-2.5 text-right font-mono text-rally-red">
                        {d.avg_pace.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      )}

      {/* ── Stage wins ─────────────────────────────────────────────────────── */}
      {stageWins && stageWins.wins.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-base font-semibold text-white">Etapas ganadas</h2>
          <div className="card overflow-hidden p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-surface-border text-xs text-zinc-500 uppercase tracking-wider">
                    <th className="px-4 py-3 text-left">Piloto</th>
                    <th className="px-4 py-3 text-left">Fabricante</th>
                    <th className="px-4 py-3 text-right">Victorias</th>
                    <th className="px-4 py-3 text-left">Etapas</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-surface-border">
                  {stageWins.wins.map(w => (
                    <tr key={w.entry_id} className="hover:bg-surface-hover/50 transition-colors">
                      <td className="px-4 py-2.5 font-medium text-white">{w.driver_name}</td>
                      <td className="px-4 py-2.5 text-zinc-400">{w.manufacturer}</td>
                      <td className="px-4 py-2.5 text-right">
                        <span className="inline-flex items-center justify-center rounded-full bg-rally-gold/20 px-2.5 py-0.5 text-xs font-bold text-rally-gold">
                          {w.win_count}
                        </span>
                      </td>
                      <td className="px-4 py-2.5 font-mono text-xs text-zinc-500">
                        {w.stage_codes.join(', ')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      )}

      {!loadingWins && stageWins?.wins.length === 0 && consistencyData.length === 0 && (
        <ErrorMessage message="Sin datos de analisis para este rally. Prueba con el rally Mock (Monte Carlo 2024) o Sweden 2025." />
      )}
    </div>
  )
}
