import { useRally } from '../context/RallyContext'
import { useApi } from '../hooks/useApi'
import { api } from '../lib/api'
import { KpiCard } from '../components/ui/KpiCard'
import { LoadingSpinner, ErrorMessage } from '../components/ui/LoadingSpinner'
import type { OverallEntry } from '../types'

function positionBadge(pos: number) {
  const base = 'inline-flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold'
  if (pos === 1) return `${base} bg-rally-gold text-black`
  if (pos === 2) return `${base} bg-rally-silver text-black`
  if (pos === 3) return `${base} bg-rally-bronze text-white`
  return `${base} bg-surface-hover text-zinc-400`
}

function manufacturerColor(mfr: string) {
  const colors: Record<string, string> = {
    Toyota: 'text-red-400',
    Hyundai: 'text-blue-400',
    Ford:    'text-cyan-400',
    'M-Sport': 'text-cyan-400',
  }
  return colors[mfr] ?? 'text-zinc-400'
}

function formatGap(diff: number | null, pos: number) {
  if (pos === 1 || diff === null || diff === 0) return '—'
  return `+${diff.toFixed(1)}s`
}

export function Overview() {
  const { eventId } = useRally()

  const { data: classification, loading, error } = useApi(
    () => api.getClassification(eventId),
    [eventId],
  )

  const { data: stages } = useApi(
    () => api.getStages(eventId),
    [eventId],
  )

  if (loading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} />
  if (!classification) return null

  const entries: OverallEntry[] = classification.entries
  const leader = entries[0]
  const p2 = entries[1]
  const margin = p2?.diff_first_s != null ? `+${p2.diff_first_s.toFixed(1)}s` : '—'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Overview</h1>
        <p className="mt-1 text-sm text-zinc-500">
          Final classification — {classification.stage_code}
        </p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <KpiCard
          label="Winner"
          value={leader?.driver_name ?? '—'}
          sub={leader?.total_time_str ?? ''}
          accent
          icon="🏆"
        />
        <KpiCard
          label="Lead margin"
          value={margin}
          sub="gap P1 → P2"
          icon="⏱"
        />
        <KpiCard
          label="Drivers"
          value={entries.length}
          sub="finishers"
          icon="👤"
        />
        <KpiCard
          label="Stages"
          value={stages?.length ?? '—'}
          sub={stages ? `${stages.reduce((a, s) => a + s.distance_km, 0).toFixed(1)} km` : ''}
          icon="🗺"
        />
      </div>

      {/* Classification table */}
      <div className="card overflow-hidden p-0">
        <div className="border-b border-surface-border px-5 py-4">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-zinc-400">
            Final Classification
          </h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-surface-border text-xs font-medium uppercase tracking-wider text-zinc-500">
                <th className="px-5 py-3 text-left">Pos</th>
                <th className="px-5 py-3 text-left">No.</th>
                <th className="px-5 py-3 text-left">Driver</th>
                <th className="px-5 py-3 text-left">Manufacturer</th>
                <th className="px-5 py-3 text-right">Total Time</th>
                <th className="px-5 py-3 text-right">Gap</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {entries.map((entry) => (
                <tr
                  key={entry.entry_id}
                  className="transition-colors hover:bg-surface-hover/50"
                >
                  <td className="px-5 py-3">
                    <span className={positionBadge(entry.position)}>
                      {entry.position}
                    </span>
                  </td>
                  <td className="px-5 py-3 font-mono text-xs text-zinc-500">
                    #{entry.car_number}
                  </td>
                  <td className="px-5 py-3 font-medium text-white">
                    {entry.driver_name}
                  </td>
                  <td className={`px-5 py-3 font-medium ${manufacturerColor(entry.manufacturer)}`}>
                    {entry.manufacturer}
                  </td>
                  <td className="px-5 py-3 text-right font-mono text-zinc-300">
                    {entry.total_time_str ?? '—'}
                  </td>
                  <td className="px-5 py-3 text-right font-mono text-zinc-500">
                    {formatGap(entry.diff_first_s, entry.position)}
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
