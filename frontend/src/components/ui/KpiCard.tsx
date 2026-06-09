interface KpiCardProps {
  label: string
  value: string | number
  sub?: string
  accent?: boolean
  icon?: string
}

export function KpiCard({ label, value, sub, accent = false, icon }: KpiCardProps) {
  return (
    <div
      className={`card flex flex-col gap-1 transition-colors hover:border-zinc-600 ${
        accent ? 'border-rally-red/40' : ''
      }`}
    >
      <div className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-zinc-500">
        {icon && <span>{icon}</span>}
        {label}
      </div>
      <div
        className={`text-2xl font-bold ${accent ? 'text-rally-red' : 'text-white'}`}
      >
        {value}
      </div>
      {sub && <div className="text-xs text-zinc-500">{sub}</div>}
    </div>
  )
}
