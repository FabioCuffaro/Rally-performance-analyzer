import { useEffect } from 'react'
import { useRally } from '../context/RallyContext'
import { api } from '../lib/api'

export function Navbar() {
  const { eventId, setEventId, rallies, setRallies } = useRally()

  useEffect(() => {
    api.getRallies().then(setRallies).catch(console.error)
  }, [setRallies])

  return (
    <header className="flex h-14 items-center justify-between border-b border-surface-border bg-surface-card px-6">
      <div className="flex items-center gap-2 text-sm text-zinc-400">
        <span className="text-rally-red font-bold text-base">●</span>
        <span className="font-medium text-white">
          {rallies.find(r => r.event_id === eventId)?.name ?? 'Loading...'}
        </span>
      </div>

      {/* Rally selector */}
      <div className="flex items-center gap-3">
        <label className="text-xs font-medium uppercase tracking-wider text-zinc-500">
          Rally
        </label>
        <select
          value={eventId}
          onChange={e => setEventId(Number(e.target.value))}
          className="rounded-lg border border-surface-border bg-surface-hover px-3 py-1.5 text-sm text-white focus:border-rally-red focus:outline-none"
        >
          {rallies.map(r => (
            <option key={r.event_id} value={r.event_id}>
              {r.name}
            </option>
          ))}
        </select>
      </div>
    </header>
  )
}
