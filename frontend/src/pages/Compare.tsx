import { useState, useMemo } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import { useRally } from '../context/RallyContext'
import { useApi } from '../hooks/useApi'
import { api } from '../lib/api'
import { LoadingSpinner, ErrorMessage } from '../components/ui/LoadingSpinner'
import type { DriverComparison } from '../types'

const COLOR_A = '#ef4444'
const COLOR_B = '#3b82f6'

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg border border-surface-border bg-surface-card px-3 py-2 text-xs shadow-xl">
      <p className="mb-1 font-semibold text-white">{label}</p>
      {payload.map((p: any) => (
        <div key={p.name} className="flex items-center justify-between gap-6">
          <span style={{ color: p.color }}>{p.name}</span>
          <span className="font-mono text-white">{p.value?.toFixed(1)}s</span>
        </div>
      ))}
      {payload.length === 2 && payload[0].value && payload[1].value && (
        <div className="mt-1 border-t border-surface-border pt-1 font-mono text-zinc-400">
          Delta: {(payload[0].value - payload[1].value).toFixed(1)}s
        </div>
      )}
    </div>
  )
}

export function Compare() {
  const { eventId } = useRally()
  const [entryA, setEntryA] = useState<number | null>(null)
  const [entryB, setEntryB] = useState<number | null>(null)

  const { data: drivers, loading: loadingDrivers } = useApi(
    () => api.getDrivers(eventId),
    [eventId],
  )

  // Default to first two drivers
  const driverA = entryA ?? drivers?.[0]?.entry_id ?? null
  const driverB = entryB ?? drivers?.[1]?.entry_id ?? null

  const { data: comparison, loading, error } = useApi(
    () =>
      driverA && driverB
        ? api.compareDrivers(driverA, driverB, eventId)
        : Promise.resolve(null),
    [driverA, driverB, eventId],
  )

  const chartData = useMemo(() => {
    if (!comparison) return []
    const allStages = Array.from(
      new Set([
        ...comparison.stage_times_a.map(s => s.stage_code),
        ...comparison.stage_times_b.map(s => s.stage_code),
      ])
    )
    return allStages.map(code => {
      const a = comparison.stage_times_a.find(s => s.stage_code === code)
      const b = comparison.stage_times_b.find(s => s.stage_code === code)
      return {
        stage: code,
        [comparison.driver_a.driver_name]: a?.time_s ?? null,
        [comparison.driver_b.driver_name]: b?.time_s ?? null,
        delta: a?.time_s && b?.time_s ? +(a.time_s - b.time_s).toFixed(1) : null,
        winnerA: a?.time_s && b?.time_s && a.time_s <= b.time_s,
      }
    })
  }, [comparison])

  // Head-to-head stats
  const h2h = useMemo(() => {
    if (!comparison) return null
    let winsA = 0, winsB = 0
    chartData.forEach(row => {
      const a = row[comparison.driver_a.driver_name] as number | null
      const b = row[comparison.driver_b.driver_name] as number | null
      if (a && b) { a < b ? winsA++ : winsB++ }
    })
    return { winsA, winsB }
  }, [chartData, comparison])

  if (loadingDrivers) return <LoadingSpinner />

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Driver Comparison</h1>
        <p className="mt-1 text-sm text-zinc-500">Comparativa de tiempos por etapa entre dos pilotos</p>
      </div>

      {/* Driver selectors */}
      <div className="grid grid-cols-2 gap-4">
        <div className="card border-red-900/40 p-4">
          <label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-red-400">
            Piloto A
          </label>
          <select
            value={driverA ?? ''}
            onChange={e => setEntryA(Number(e.target.value))}
            className="w-full rounded-lg border border-surface-border bg-surface-hover px-3 py-2 text-sm text-white focus:border-rally-red focus:outline-none"
          >
            {drivers?.map(d => (
              <option key={d.entry_id} value={d.entry_id}>
                #{d.car_number} {d.driver_name}
              </option>
            ))}
          </select>
        </div>
        <div className="card border-blue-900/40 p-4">
          <label className="mb-2 block text-xs font-semibold uppercase tracking-wider text-blue-400">
            Piloto B
          </label>
          <select
            value={driverB ?? ''}
            onChange={e => setEntryB(Number(e.target.value))}
            className="w-full rounded-lg border border-surface-border bg-surface-hover px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none"
          >
            {drivers?.map(d => (
              <option key={d.entry_id} value={d.entry_id}>
                #{d.car_number} {d.driver_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message="Sin datos de tiempos de etapa para este rally." />}

      {comparison && chartData.length > 0 && (
        <>
          {/* H2H summary */}
          {h2h && (
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="card border-red-900/40 p-4">
                <div className="text-3xl font-bold text-rally-red">{h2h.winsA}</div>
                <div className="mt-1 text-xs text-zinc-500">etapas</div>
                <div className="mt-1 text-sm font-medium text-white truncate">
                  {comparison.driver_a.driver_name}
                </div>
              </div>
              <div className="card flex flex-col items-center justify-center p-4">
                <div className="text-xl font-bold text-zinc-400">H2H</div>
                <div className="text-xs text-zinc-600">{chartData.length} etapas</div>
              </div>
              <div className="card border-blue-900/40 p-4">
                <div className="text-3xl font-bold text-blue-400">{h2h.winsB}</div>
                <div className="mt-1 text-xs text-zinc-500">etapas</div>
                <div className="mt-1 text-sm font-medium text-white truncate">
                  {comparison.driver_b.driver_name}
                </div>
              </div>
            </div>
          )}

          {/* Grouped bar chart */}
          <div className="card p-4">
            <h2 className="mb-4 text-xs font-semibold uppercase tracking-wider text-zinc-500">
              Tiempo por etapa (s)
            </h2>
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={chartData} margin={{ left: 0, right: 16, top: 4, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                <XAxis dataKey="stage" tick={{ fill: '#71717a', fontSize: 12 }} tickLine={false} axisLine={{ stroke: '#27272a' }} />
                <YAxis
                  domain={['dataMin - 10', 'dataMax + 10']}
                  tick={{ fill: '#71717a', fontSize: 11 }}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
                <Legend wrapperStyle={{ color: '#a1a1aa', fontSize: 12 }} />
                <Bar
                  dataKey={comparison.driver_a.driver_name}
                  fill={COLOR_A}
                  fillOpacity={0.85}
                  radius={[3, 3, 0, 0]}
                  maxBarSize={24}
                />
                <Bar
                  dataKey={comparison.driver_b.driver_name}
                  fill={COLOR_B}
                  fillOpacity={0.85}
                  radius={[3, 3, 0, 0]}
                  maxBarSize={24}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Delta table */}
          <div className="card overflow-hidden p-0">
            <div className="border-b border-surface-border px-5 py-3">
              <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
                Diferencia por etapa
              </h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-surface-border text-xs text-zinc-500 uppercase tracking-wider">
                    <th className="px-4 py-3 text-left">Etapa</th>
                    <th className="px-4 py-3 text-right" style={{ color: COLOR_A }}>
                      {comparison.driver_a.driver_name}
                    </th>
                    <th className="px-4 py-3 text-right" style={{ color: COLOR_B }}>
                      {comparison.driver_b.driver_name}
                    </th>
                    <th className="px-4 py-3 text-right">Delta</th>
                    <th className="px-4 py-3 text-left">Ganador</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-surface-border">
                  {chartData.map(row => {
                    const a = row[comparison.driver_a.driver_name] as number | null
                    const b = row[comparison.driver_b.driver_name] as number | null
                    const delta = row.delta as number | null
                    const aWins = row.winnerA as boolean
                    return (
                      <tr key={row.stage} className="hover:bg-surface-hover/50 transition-colors">
                        <td className="px-4 py-2.5 font-medium text-white">{row.stage}</td>
                        <td className="px-4 py-2.5 text-right font-mono text-zinc-300">{a?.toFixed(1) ?? '—'}s</td>
                        <td className="px-4 py-2.5 text-right font-mono text-zinc-300">{b?.toFixed(1) ?? '—'}s</td>
                        <td className={`px-4 py-2.5 text-right font-mono font-medium ${
                          delta === null ? 'text-zinc-600'
                          : delta < 0 ? 'text-rally-red'
                          : delta > 0 ? 'text-blue-400'
                          : 'text-zinc-400'
                        }`}>
                          {delta !== null ? (delta > 0 ? `+${delta}` : `${delta}`) + 's' : '—'}
                        </td>
                        <td className="px-4 py-2.5 text-xs font-medium" style={{ color: a && b ? (aWins ? COLOR_A : COLOR_B) : '#52525b' }}>
                          {a && b ? (aWins ? comparison.driver_a.driver_name : comparison.driver_b.driver_name) : '—'}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
