export type Action = 'good' | 'bad' | 'reset'

export interface DemoState {
  good: number | null
  bad: number | null
  logged: boolean
  tries: number
  dlq: number
  alarm: 'OK' | 'ALARM' | 'INSUFFICIENT_DATA'
  blocked: string
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/${path}`, init)
  const data = await response.json()
  if (!response.ok) throw new Error(data.error)
  return data as T
}

export const getState = () => request<DemoState>('state')

export const runAction = (action: Action) =>
  request<{ ok: boolean }>(action, { method: 'POST', headers: { 'X-Demo': '1' } })
