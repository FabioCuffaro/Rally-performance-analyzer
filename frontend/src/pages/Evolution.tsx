import { useState, useMemo } from 'react'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import { useRally } from '../context/RallyContext'
import { useApi } from '../hooks/useApi'
import { api } from '../lib/api'
import { LoadingSpinner, ErrorMessage } from '../components/ui/LoadingSpinner'
import type { DriverEvolution } from '../types'

const LINE_COLORS = [
  '#ef4444', '#3b82f6', '#22c55e', '#f59e0b',
  '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16',
  '#f97316', '#a855f7', '#14b8a6', '#facc15',
]

type ChartMode = 'bump' | 'gap'

function buildChartData(drivers: DriverEvolution[]) {
  // Collect all stage codes in order
  const allStages = Array.from(
    new Map(
      drivers.flatMap(d => d.positions.map(p => [p.stage_id, p.stage_code]))
    )
  )
    .sort((a, b) => a[0] - b[0])
    .map(([, code]) => code)

  return allStages.map(stageCode => {
    const row: Record<string, string | number> = { stage: stageCode }
    drivers.forEach(d => {
      const pos = d.positions.find(p => p.stage_code === stageCode)
      if (pos) {
        row[`pos_${d.entry_id}`] = pos.position
        row[`gap_${d.entry_id}`] = pos.diff_first_s ?? 0
      }
    })
    return row
  })
}

const CustomTooltip = ({
  active, payload, label, mode, drivers,
}: any) => {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg border border-surface-border bg-surface-card px-3 py-2 text-xs shadow-xl min-w-[140px]">
      <p className="mb-1 font-semibold text-white">{label}</p>
      {payload.map((p: any) => {
        const entryId = Number(p.dataKey.split('_')[1])
        const driver = drivers.find((d: DriverEvolution) => d.entry_id === entryId)
        return (
          <div key={p.dataKey} className="flex items-center justify-between gap-4">
            <span style={{ color: p.color }}>{driver?.driver_name ?? p.dataKey}</span>
            <span className="font-mono text-white">
              {mode === 'bump' ? `P${p.value}` : `+${Number(p.value).toFixed(1)}s`}
            </span>
          </div>
        )
      })}
    </div>
  )
}

export function Evolution() {
  const { eventId } = useRally()
  const [mode, setMode] = useState<ChartMode>('bump')
  const [visibleIds, setVisibleIds] = useState<Set<number> | null>(null)

  const { data: evolution, loading, error } = useApi(
    () => api.getEvolution(eventId),
    [eventId],
  )

  // Default: show top 10 by final position
  const sortedDrivers = useMemo(() => {
    if (!evolution) return []
    return [...evolution].sort((a, b) => {
      const posA = a.positions.at(-1)?.position ?? 99
      const posB = b.positions.at(-1)?.position ?? 99
      return posA - posB
    })
  }, [evolution])

  const top10Ids = useMemo(() => new Set(sortedDrivers.slice(0, 10).map(d => d.entry_id)), [sortedDrivers])
  const activeIds = visibleIds ?? top10Ids
  const visibleDrivers = sortedDrivers.filter(d => activeIds.has(d.entry_id))

  const chartData = useMemo(() => buildChartData(visibleDrivers), [visibleDrivers])
  const hasMultipleStages = (evolution?.[0]?.positions.length ?? 0) > 1

  function toggleDriver(id: number) {
    const current = visibleIds ?? top10Ids
    const next = new Set(current)
    if (next.has(id)) { next.delete(id) } else { next.add(id) }
    setVisibleIds(next)
  }

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />
  if (!evolution?.length) return <ErrorMessage message="Sin datos de evolucion para este rally." />

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Position Evolution</h1>
          <p className="mt-1 text-sm text-zinc-500">Evolucion de posiciones a lo largo del rally</p>
        </div>
        {/* Mode toggle */}
        <div className="flex rounded-lg border border-surface-border overflow-hidden text-sm">
          {(['bump', 'gap'] as ChartMode[]).map(m => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={`px-4 py-2 font-medium transition-colors ${
                mode === m
                  ? 'bg-rally-red text-white'
                  : 'bg-surface-card text-zinc-400 hover:text-white'
              }`}
            >
              {m === 'bump' ? '📈 Posicion' : '⏱ Gap'}
            </button>
          ))}
        </div>
      </div>

      {!hasMultipleStages && (
        <div className="rounded-lg border border-yellow-900 bg-yellow-950/30 px-4 py-3 text-sm text-yellow-400">
          ⚠ Este rally solo tiene datos de clasificacion final. El grafico de evolucion requiere datos por etapa.
        </div>
      )}

      {/* Driver filter */}
      <div className="card p-4">
        <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">
          Pilotos visibles ({activeIds.size}/{sortedDrivers.length})
        </p>
        <div className="flex flex-wrap gap-2">
          {sortedDrivers.map((d, i) => {
            const color = LINE_COLORS[i % LINE_COLORS.length]
            const active = activeIds.has(d.entry_id)
            return (
              <button
                key={d.entry_id}
                onClick={() => toggleDriver(d.entry_id)}
                className={`flex items-center gap-1.5 rounded-lg border px-2.5 py-1 text-xs font-medium transition-all ${
                  active
                    ? 'border-transparent text-white'
                    : 'border-surface-border text-zinc-600 hover:text-zinc-400'
                }`}
                style={active ? { backgroundColor: `${color}22`, borderColor: color } : {}}
              >
                <span
                  className="h-2 w-2 rounded-full flex-shrink-0"
                  style={{ backgroundColor: active ? color : '#3f3f46' }}
                />
                {d.driver_name}
              </button>
            )
          })}
        </div>
      </div>

      {/* Chart */}
      <div className="card p-4">
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData} margin={{ left: 0, right: 16, top: 8, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
            <XAxis
              dataKey="stage"
              tick={{ fill: '#71717a', fontSize: 12 }}
              tickLine={false}
              axisLine={{ stroke: '#27272a' }}
            />
            <YAxis
              reversed={mode === 'bump'}
              tick={{ fill: '#71717a', fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              domain={mode === 'bump' ? [1, 'dataMax'] : [0, 'dataMax']}
              tickFormatter={v => mode === 'bump' ? `P${v}` : `+${v}s`}
            />
            <Tooltip
              content={<CustomTooltip mode={mode} drivers={visibleDrivers} />}
            />
            {visibleDrivers.map((d, i) => (
              <Line
                key={d.entry_id}
                type="monotone"
                dataKey={mode === 'bump' ? `pos_${d.entry_id}` : `gap_${d.entry_id}`}
                stroke={LINE_COLORS[i % LINE_COLORS.length]}
                strokeWidth={2}
                dot={{ r: 3, fill: LINE_COLORS[i % LINE_COLORS.length] }}
                activeDot={{ r: 5 }}
                connectNulls
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Quick stats table */}
      <div className="card overflow-hidden p-0">
        <div className="border-b border-surface-border px-5 py-3">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
            Clasificacion final
          </h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-border text-xs text-zinc-500 uppercase tracking-wider">
                <th className="px-4 py-3 text-left">Final Pos</th>
                <th className="px-4 py-3 text-left">Piloto</th>
                <th className="px-4 py-3 text-left">Fabricante</th>
                <th className="px-4 py-3 text-right">Etapas</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {sortedDrivers.slice(0, 15).map((d, i) => {
                const finalPos = d.positions.at(-1)?.position ?? '—'
                return (
                  <tr key={d.entry_id} className="hover:bg-surface-hover/50 transition-colors">
                    <td className="px-4 py-2.5 font-bold" style={{ color: LINE_COLORS[i % LINE_COLORS.length] }}>
                      P{finalPos}
                    </td>
                    <td className="px-4 py-2.5 font-medium text-white">{d.driver_name}</td>
                    <td className="px-4 py-2.5 text-zinc-400">{d.manufacturer}</td>
                    <td className="px-4 py-2.5 text-right font-mono text-zinc-500">{d.positions.length}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
