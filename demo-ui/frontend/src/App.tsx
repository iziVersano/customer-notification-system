import { useCallback, useEffect, useState } from 'react'
import { getState, shipOrder, type DemoState } from './api'
import { Order } from './Order'

export function App() {
  const [state, setState] = useState<DemoState>()
  const [offline, setOffline] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const refresh = useCallback(async () => {
    try {
      setState(await getState())
      setOffline('')
    } catch (e) {
      setOffline(`Not connected: ${(e as Error).message}`)
    }
  }, [])

  useEffect(() => {
    void refresh()
    const timer = setInterval(refresh, 4000)
    return () => clearInterval(timer)
  }, [refresh])

  async function ship() {
    setBusy(true)
    setError('')
    try {
      await shipOrder()
      await refresh()
    } catch (e) {
      setError((e as Error).message)
    }
    setBusy(false)
  }

  if (!state) return <main>{offline || 'Connecting…'}</main>

  const disabled = busy || offline !== ''

  return (
    <main>
      <h1>NotifyNow orders</h1>
      <p className="muted">Simulated app, real AWS</p>
      {(offline || error) && <p role="alert" className="error">{offline || error}</p>}

      <Order
        id="A-2001"
        customer="Lena Hoffmann"
        disabled={disabled}
        onShip={ship}
        steps={[
          { label: 'Sent to SNS', done: state.good !== null },
          { label: 'Logged by Lambda', done: state.logged },
        ]}
      />
    </main>
  )
}
