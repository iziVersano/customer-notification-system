# Architecture Options

Both options use SNS as the single place the app publishes to. The difference is what sits between SNS and the code that sends the notification.

## Option A: SNS → SQS → Lambda (fan-out with queues)

```
App ──publish──> SNS topic "customer-events"
                    ├──> Email subscription ──> my inbox
                    └──> SQS "notifications" ──> Lambda ──> logs (SMS / internal, simulated)
                              └── after 3 failures ──> SQS DLQ
```

- Each code-based consumer gets its own queue.
- Lambda reads from the queue in batches. If it fails, the message goes back to the queue and is retried.
- After 3 failed tries the message moves to a dead-letter queue (DLQ), where it can be inspected and replayed.

## Option B: SNS → Lambda directly

```
App ──publish──> SNS topic "customer-events"
                    ├──> Email subscription ──> my inbox
                    └──> Lambda ──> logs (SMS / internal, simulated)
                           └── after async retries ──> DLQ (on-failure destination)
```

- SNS calls the Lambda directly. No queue in between.
- Lambda retries failed async calls twice, then can send the event to a DLQ.

## Comparison

| | Option A (with SQS) | Option B (direct) |
|---|---|---|
| Moving parts | Topic, queue, DLQ, Lambda | Topic, Lambda, DLQ |
| Buffer during spikes or outages | Yes, messages wait in the queue (up to 14 days) | No real buffer |
| Retry control | Configurable (max receives, visibility timeout) | Fixed: 2 retries |
| Batching | Yes, up to 10 messages per Lambda call | One event per call |
| Failure isolation | Strong: one queue per consumer | Weaker |
| Seeing the backlog | Queue depth in CloudWatch | Not visible |
| Cost | Free tier, a few extra SQS requests | Free tier |
| Effort | A bit more Terraform | Least |

## Decision

**Option A.** It costs almost nothing extra and covers the requirements B handles poorly: messages are not lost when the consumer is down, retries are configurable, and the dead-letter queue and queue depth give clear visibility. The brief's week 3 work (retry, DLQ, monitoring) also builds directly on it.

Option B stays a valid choice for a simple consumer where losing an event now and then is acceptable.
