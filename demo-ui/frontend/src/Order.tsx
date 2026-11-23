interface Step {
  label: string
  done: boolean
  failed?: boolean
}

interface OrderProps {
  id: string
  customer: string
  steps: Step[]
  disabled: boolean
  hint?: string
  onShip: () => void
}

export function Order({ id, customer, steps, disabled, hint, onShip }: OrderProps) {
  return (
    <section>
      <header>
        <div>
          <h2>Order {id}</h2>
          <span className="muted">{customer}</span>
        </div>
        <button onClick={onShip} disabled={disabled}>Ship order</button>
      </header>
      {hint && <p className="muted">{hint}</p>}
      <ul>
        {steps.map(({ label, done, failed }, index) => (
          <li key={index} className={done ? (failed ? 'failed' : 'done') : ''}>{label}</li>
        ))}
      </ul>
    </section>
  )
}
