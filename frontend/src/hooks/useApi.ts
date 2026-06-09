import { useState, useEffect, useCallback } from 'react'

interface ApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

/**
 * Generic hook for API calls.
 * Re-fetches automatically when `deps` change.
 *
 * @example
 * const { data, loading, error } = useApi(
 *   () => api.getClassification(eventId),
 *   [eventId]
 * )
 */
export function useApi<T>(
  fetcher: () => Promise<T>,
  deps: unknown[],
): ApiState<T> & { refetch: () => void } {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: true,
    error: null,
  })

  const fetchData = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }))
    try {
      const data = await fetcher()
      setState({ data, loading: false, error: null })
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Error desconocido'
      setState({ data: null, loading: false, error: msg })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return { ...state, refetch: fetchData }
}
