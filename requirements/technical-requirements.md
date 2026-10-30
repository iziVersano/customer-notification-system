# Technical Requirements

## Functional

| # | Requirement |
|---|---|
| F1 | The app publishes an event with a type, IDs and a timestamp (example: `OrderCreated`). |
| F2 | Every event reaches at least two independent consumers. |
| F3 | At least one consumer reads from a queue and processes the event in code. |
| F4 | Consumers work asynchronously. The app does not wait for them. |
| F5 | A failed message is retried automatically. |
| F6 | A message that fails again and again moves to a dead-letter queue. |
| F7 | Every processed and failed message is logged. |

## Non-functional

| Area | Requirement |
|---|---|
| Decoupling | The app only knows one topic, not the consumers. |
| Reliability | A failing consumer does not block the app or the other consumers. Messages are not lost. |
| Scalability | Handles bursts of events without changing the setup. |
| Security | Each part gets only the permissions it needs. No personal data beyond IDs in messages. |
| Observability | Logs and alarms for errors and for messages in the dead-letter queue. |
| Cost | Fits the AWS free tier. No servers running all the time. |
| Reproducible | Everything is created and destroyed with Terraform. |
