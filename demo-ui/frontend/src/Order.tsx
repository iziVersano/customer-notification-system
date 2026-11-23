interface Step {
  label: string
  done: boolean
}

interface OrderProps {
  id: string
  customer: string
  steps: Step[]
  disabled: boolean
  onShip: () => void
}

export function Order({ id, customer, steps, disabled, onShip }: OrderProps) {
  return (
    <section>
      <header>
        <div>
          <h2>Order {id}</h2>
          <span className="muted">{customer}</span>
        </div>
        <button onClick={onShip} disabled={disabled}>Ship order</button>
      </header>
      <ul>
        {steps.map(({ label, done }, index) => (
          <li key={index} className={done ? 'done' : ''}>{label}</li>
        ))}
      </ul>
    </section>
  )
}
