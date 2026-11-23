export interface DemoState {
  good: number | null
  logged: boolean
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/${path}`, init)
  const data = await response.json()
  if (!response.ok) throw new Error(data.error)
  return data as T
}

export const getState = () => request<DemoState>('state')

export const shipOrder = () =>
  request<{ ok: boolean }>('good', { method: 'POST', headers: { 'X-Demo': '1' } })
