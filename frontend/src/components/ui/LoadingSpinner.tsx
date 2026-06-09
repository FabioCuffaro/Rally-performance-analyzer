export function LoadingSpinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizes = { sm: 'h-4 w-4', md: 'h-8 w-8', lg: 'h-12 w-12' }
  return (
    <div className="flex items-center justify-center py-12">
      <div
        className={`${sizes[size]} animate-spin rounded-full border-2 border-surface-border border-t-rally-red`}
      />
    </div>
  )
}

export function ErrorMessage({ message }: { message: string }) {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-red-900 bg-red-950/30 px-4 py-3 text-sm text-red-400">
      <span className="text-lg">⚠</span>
      <span>{message}</span>
    </div>
  )
}
