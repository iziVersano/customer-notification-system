import { useCallback, useEffect, useState } from 'react'
import { getState, runAction, type Action, type DemoState } from './api'
import { Order } from './Order'

export function App() {
  const [state, setState] = useState<DemoState>()
  const [offline, setOffline] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [confirming, setConfirming] = useState(false)

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

  async function run(action: Action) {
    setBusy(true)
    setError('')
    setConfirming(false)
    try {
      await runAction(action)
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
        onShip={() => run('good')}
        steps={[
          { label: 'Sent to SNS', done: state.good !== null },
          { label: 'Logged by Lambda', done: state.logged },
        ]}
      />

      <Order
        id="A-2002"
        customer="No email address"
        disabled={disabled || state.blocked !== ''}
        hint={state.blocked}
        onShip={() => run('bad')}
        steps={[
          { label: 'Sent to SNS', done: state.bad !== null },
          { label: `Failed tries: ${state.tries} of 3`, done: state.tries === 3, failed: true },
          { label: `Dead-letter queue: ${state.dlq}`, done: state.dlq > 0, failed: true },
          { label: `Alarm: ${state.alarm}`, done: state.alarm === 'ALARM', failed: true },
        ]}
      />

      {confirming ? (
        <div className="confirm">
          <span>Permanently delete the failed messages?</span>
          <button onClick={() => run('reset')} disabled={disabled}>Delete</button>
          <button className="link" onClick={() => setConfirming(false)}>Cancel</button>
        </div>
      ) : (
        <button className="link" onClick={() => setConfirming(true)} disabled={disabled || state.dlq === 0}>
          Reset demo
        </button>
      )}
    </main>
  )
}
