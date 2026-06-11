import { useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer, LineChart, Line,
} from 'recharts'
import { useApi } from '../hooks/useApi'
import { api } from '../lib/api'
import { LoadingSpinner, ErrorMessage } from '../components/ui/LoadingSpinner'
import type { SeasonStandingsEntry, DriverSeasonPace, SeasonSurfaceEntry } from '../types'

const EVENT_IDS = '89918,90090'
const MOCK_IDS  = '1'

const MFR_COLORS: Record<string, string> = {
  Toyota: '#ef4444', Hyundai: '#3b82f6',
  Ford: '#06b6d4', 'M-Sport': '#06b6d4',
}
const LINE_COLORS = [
  '#ef4444','#3b82f6','#22c55e','#f59e0b',
  '#8b5cf6','#ec4899','#06b6d4','#84cc16',
]

type Tab = 'standings' | 'pace' | 'surface'

const StandingsTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg border border-surface-border bg-surface-card px-3 py-2 text-xs shadow-xl">
      <p className="font-bold text-white">{label}</p>
      {payload.map((p: any) => (
        <div key={p.name} className="flex justify-between gap-4">
          <span style={{ color: p.fill }}>{p.name}</span>
          <span className="font-mono text-white">{p.value} pts</span>
        </div>
      ))}
    </div>
  )
}

function StandingsTab() {
  const { data: standings, loading, error } = useApi(
    () => api.getSeasonStandings(EVENT_IDS), [EVENT_IDS]
  )

  if (loading) return <LoadingSpinner />
  if (error || !standings?.entries.length)
    return <ErrorMessage message="Sin datos de standings. Los eventos reales WRC 2025 tienen clasificacion disponible." />

  const top15 = standings.entries.slice(0, 15)

  // Build chart data: one bar per driver showing points per event
  const eventCols = standings.entries[0]
    ? Object.keys(standings.entries[0].rally_points)
    : []

  const chartData = top15.map(e => ({
    name: e.driver_name.split(' ')[0],  // apellido solo
    total: e.total_points,
    manufacturer: e.manufacturer,
    ...Object.fromEntries(
      Object.entries(e.rally_points).map(([k, v]) => [`pts_${k}`, v])
    ),
  }))

  return (
    <div className="space-y-6">
      {/* KPIs */}
      <div className="grid grid-cols-3 gap-4">
        <div className="card p-4">
          <div className="text-xs text-zinc-500 uppercase tracking-wider">Lider</div>
          <div className="mt-1 font-bold text-white">{top15[0]?.driver_name}</div>
          <div className="text-xs text-zinc-400">{top15[0]?.manufacturer}</div>
        </div>
        <div className="card p-4">
          <div className="text-xs text-zinc-500 uppercase tracking-wider">Puntos lider</div>
          <div className="mt-1 text-2xl font-bold text-rally-red">{top15[0]?.total_points}</div>
        </div>
        <div className="card p-4">
          <div className="text-xs text-zinc-500 uppercase tracking-wider">Pilotos en puntos</div>
          <div className="mt-1 text-2xl font-bold text-white">{standings.entries.length}</div>
        </div>
      </div>

      {/* Bar chart */}
      <div className="card p-4">
        <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-zinc-500">
          Puntos totales — Top 15
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData} margin={{ left: 0, right: 16, top: 4, bottom: 40 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
            <XAxis dataKey="name" tick={{ fill: '#71717a', fontSize: 11 }}
              tickLine={false} axisLine={{ stroke: '#27272a' }}
              angle={-35} textAnchor="end" interval={0}
            />
            <YAxis tick={{ fill: '#71717a', fontSize: 11 }} tickLine={false} axisLine={false} />
            <Tooltip content={<StandingsTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
            <Legend wrapperStyle={{ color: '#a1a1aa', fontSize: 11, paddingTop: 16 }} />
            {eventCols.map((eid, i) => (
              <Bar key={eid} dataKey={`pts_${eid}`} name={`Event ${eid}`}
                fill={LINE_COLORS[i % LINE_COLORS.length]} fillOpacity={0.85}
                stackId="a" radius={i === eventCols.length - 1 ? [4, 4, 0, 0] : undefined}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Table */}
      <div className="card overflow-hidden p-0">
        <div className="border-b border-surface-border px-5 py-3">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
            Clasificacion de temporada
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-border text-xs text-zinc-500 uppercase tracking-wider">
                <th className="px-4 py-3 text-left">Pos</th>
                <th className="px-4 py-3 text-left">Piloto</th>
                <th className="px-4 py-3 text-left">Fabricante</th>
                {eventCols.map(eid => (
                  <th key={eid} className="px-4 py-3 text-right">Event {eid}</th>
                ))}
                <th className="px-4 py-3 text-right font-bold text-white">Total</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {top15.map((entry, i) => (
                <tr key={entry.driver_name} className="hover:bg-surface-hover/50 transition-colors">
                  <td className="px-4 py-2.5 font-bold text-zinc-400">{i + 1}</td>
                  <td className="px-4 py-2.5 font-medium text-white">{entry.driver_name}</td>
                  <td className="px-4 py-2.5 text-sm"
                    style={{ color: MFR_COLORS[entry.manufacturer] ?? '#71717a' }}>
                    {entry.manufacturer}
                  </td>
                  {eventCols.map(eid => (
                    <td key={eid} className="px-4 py-2.5 text-right font-mono text-zinc-400">
                      {entry.rally_points[eid] ?? 0}
                    </td>
                  ))}
                  <td className="px-4 py-2.5 text-right font-bold font-mono text-rally-red">
                    {entry.total_points}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function PaceTab() {
  const { data, loading, error } = useApi(
    () => api.getSeasonPaceEvolution(MOCK_IDS), [MOCK_IDS]
  )

  if (loading) return <LoadingSpinner />

  if (error || !data?.length)
    return <ErrorMessage message="Sin datos de pace en eventos reales. Usando mock (Monte Carlo 2024) para demo." />

  const top8 = data.slice(0, 8)

  // Build chart data: one point per driver per rally
  const allEvents = Array.from(new Set(
    top8.flatMap(d => d.paces.map(p => p.event_name))
  ))

  const chartData = allEvents.map(eName => {
    const row: Record<string, string | number> = { event: eName }
    top8.forEach(d => {
      const p = d.paces.find(x => x.event_name === eName)
      if (p) row[d.driver_name.split(' ')[0]] = p.avg_pace
    })
    return row
  })

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-yellow-900 bg-yellow-950/30 px-4 py-3 text-xs text-yellow-400">
        ⚡ Mostrando datos del rally mock (Monte Carlo 2024). Los eventos WRC 2025 reales no tienen tiempos por etapa completos todavia.
      </div>
      <div className="card p-4">
        <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-zinc-500">
          Pace medio (s/km) por piloto y rally
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={chartData} margin={{ left: 0, right: 16, top: 8, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
            <XAxis dataKey="event" tick={{ fill: '#71717a', fontSize: 11 }} tickLine={false} axisLine={{ stroke: '#27272a' }} />
            <YAxis tick={{ fill: '#71717a', fontSize: 11 }} tickLine={false} axisLine={false}
              tickFormatter={v => `${v}s`} />
            <Tooltip formatter={(v: number) => [`${v.toFixed(2)} s/km`, '']}
              contentStyle={{ background: '#18181b', border: '1px solid #3f3f46', fontSize: 12 }} />
            <Legend wrapperStyle={{ color: '#a1a1aa', fontSize: 11 }} />
            {top8.map((d, i) => (
              <Line key={d.driver_name} type="monotone"
                dataKey={d.driver_name.split(' ')[0]}
                stroke={LINE_COLORS[i % LINE_COLORS.length]}
                strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} connectNulls
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

function SurfaceTab() {
  const { data, loading, error } = useApi(
    () => api.getSeasonSurfaceMastery(MOCK_IDS), [MOCK_IDS]
  )

  if (loading) return <LoadingSpinner />
  if (error || !data?.length)
    return <ErrorMessage message="Sin datos de superficie disponibles." />

  const surfaces = Array.from(new Set(data.map(d => d.surface)))
  const drivers  = Array.from(new Set(data.map(d => d.driver_name)))

  const chartData = drivers.map(driver => {
    const row: Record<string, string | number> = { driver: driver.split(' ')[0] }
    surfaces.forEach(surface => {
      const entry = data.find(d => d.driver_name === driver && d.surface === surface)
      if (entry) row[surface] = entry.avg_pace
    })
    return row
  })

  const SURFACE_COLORS: Record<string, string> = {
    Tarmac: '#f59e0b', Snow: '#93c5fd', Gravel: '#a3e635', Ice: '#67e8f9',
  }

  return (
    <div className="space-y-6">
      <div className="card p-4">
        <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-zinc-500">
          Pace medio por superficie y piloto (s/km)
        </h3>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={chartData} margin={{ left: 0, right: 16, top: 4, bottom: 8 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
            <XAxis dataKey="driver" tick={{ fill: '#71717a', fontSize: 12 }} tickLine={false} axisLine={{ stroke: '#27272a' }} />
            <YAxis domain={['dataMin - 2', 'dataMax + 2']} tick={{ fill: '#71717a', fontSize: 11 }} tickLine={false} axisLine={false}
              tickFormatter={v => `${v}s`} />
            <Tooltip formatter={(v: number) => [`${v.toFixed(2)} s/km`, '']}
              contentStyle={{ background: '#18181b', border: '1px solid #3f3f46', fontSize: 12 }} />
            <Legend wrapperStyle={{ color: '#a1a1aa', fontSize: 11 }} />
            {surfaces.map(surface => (
              <Bar key={surface} dataKey={surface}
                fill={SURFACE_COLORS[surface] ?? '#71717a'}
                fillOpacity={0.85} radius={[4, 4, 0, 0]} maxBarSize={28}
              />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export function Season() {
  const [tab, setTab] = useState<Tab>('standings')

  const TABS: { id: Tab; label: string; icon: string }[] = [
    { id: 'standings', label: 'Standings', icon: '🏆' },
    { id: 'pace',      label: 'Pace',      icon: '⚡' },
    { id: 'surface',   label: 'Superficie', icon: '🌍' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Season 2025</h1>
        <p className="mt-1 text-sm text-zinc-500">
          Analisis cross-rally — puntos FIA, pace y rendimiento por superficie
        </p>
      </div>

      {/* Tabs */}
      <div className="flex rounded-lg border border-surface-border overflow-hidden w-fit">
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-5 py-2.5 text-sm font-medium transition-colors ${
              tab === t.id
                ? 'bg-rally-red text-white'
                : 'bg-surface-card text-zinc-400 hover:text-white'
            }`}
          >
            <span>{t.icon}</span>{t.label}
          </button>
        ))}
      </div>

      {tab === 'standings' && <StandingsTab />}
      {tab === 'pace'      && <PaceTab />}
      {tab === 'surface'   && <SurfaceTab />}
    </div>
  )
}
