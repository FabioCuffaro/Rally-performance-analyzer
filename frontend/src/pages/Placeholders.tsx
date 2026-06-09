// Stages, Evolution, Compare, Analysis — implemented in Bloque 9

function ComingSoon({ title, icon }: { title: string; icon: string }) {
  return (
    <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
      <span className="text-6xl">{icon}</span>
      <h1 className="text-2xl font-bold text-white">{title}</h1>
      <p className="text-zinc-500">Coming in Bloque 9 — stay tuned 🏎</p>
    </div>
  )
}

export function Stages()    { return <ComingSoon title="Stage Times"       icon="⏱" /> }
export function Evolution() { return <ComingSoon title="Position Evolution" icon="📈" /> }
export function Compare()   { return <ComingSoon title="Driver Comparison"  icon="⚔" /> }
export function Analysis()  { return <ComingSoon title="Pace & Analysis"    icon="📊" /> }
