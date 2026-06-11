import { NavLink } from 'react-router-dom'

const NAV_ITEMS = [
  { to: '/',          label: 'Overview',   icon: '🏁' },
  { to: '/stages',    label: 'Stages',     icon: '⏱' },
  { to: '/evolution', label: 'Evolution',  icon: '📈' },
  { to: '/compare',   label: 'Compare',    icon: '⚔' },
  { to: '/analysis',  label: 'Analysis',   icon: '📊' },
  { to: '/season',    label: 'Season',     icon: '🏆' },
]

export function Sidebar() {
  return (
    <aside className="flex w-56 flex-shrink-0 flex-col border-r border-surface-border bg-surface-card">
      {/* Logo */}
      <div className="flex items-center gap-3 border-b border-surface-border px-5 py-5">
        <span className="text-2xl">🏎</span>
        <div>
          <p className="text-sm font-bold leading-tight text-white">Rally</p>
          <p className="text-xs leading-tight text-zinc-500">Performance Analyzer</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex flex-1 flex-col gap-1 p-3">
        {NAV_ITEMS.map(item => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-rally-red/10 text-rally-red'
                  : 'text-zinc-400 hover:bg-surface-hover hover:text-white'
              }`
            }
          >
            <span className="text-base">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-surface-border p-4 text-xs text-zinc-600">
        WRC Data Dashboard v3.0
      </div>
    </aside>
  )
}
