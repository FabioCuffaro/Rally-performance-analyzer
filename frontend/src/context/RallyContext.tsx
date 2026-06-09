import { createContext, useContext, useState, type ReactNode } from 'react'
import type { EventSummary } from '../types'

interface RallyContextValue {
  eventId: number
  setEventId: (id: number) => void
  rallies: EventSummary[]
  setRallies: (rallies: EventSummary[]) => void
}

const RallyContext = createContext<RallyContextValue | null>(null)

export function RallyProvider({ children }: { children: ReactNode }) {
  const [eventId, setEventId] = useState<number>(89918)  // Monte Carlo 2025 por defecto
  const [rallies, setRallies] = useState<EventSummary[]>([])

  return (
    <RallyContext.Provider value={{ eventId, setEventId, rallies, setRallies }}>
      {children}
    </RallyContext.Provider>
  )
}

export function useRally(): RallyContextValue {
  const ctx = useContext(RallyContext)
  if (!ctx) throw new Error('useRally must be used inside RallyProvider')
  return ctx
}
