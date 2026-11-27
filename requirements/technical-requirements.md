# Technical Requirements

## Functional

- The app publishes an event with a type, IDs and a timestamp, e.g. `OrderCreated`.
- Each event reaches at least two consumers.
- At least one consumer reads from a queue and handles the event in code.
- The app doesn't wait for the consumers.
- Failed messages are retried.
- Messages that keep failing go to a dead-letter queue.
- Processing and failures are logged.
- An alarm goes off when messages reach the dead-letter queue.

## Non-functional

- The app only knows the topic, not the consumers.
- One broken consumer doesn't affect the others.
- Handles bursts without changing the setup.
- Each part only gets the permissions it needs.
- No personal data in messages, just IDs. Events carry `orderId` and `customerId`; the Lambda logs those identifiers, not contact details.
- Stays in the free tier, with no servers running all the time. Email is free only up to 1,000 a month.
- Everything is created and destroyed with Terraform.
