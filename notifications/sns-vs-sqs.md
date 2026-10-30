# SNS vs SQS

## Key terms

- **Event:** a fact that happened, like "order ORD-1001 was created".
- **Publish/subscribe:** the sender publishes to a topic. Anyone interested subscribes to the topic. Sender and receivers don't know each other.
- **Fan-out:** one published message is copied to every subscriber.

## Comparison

| | SNS (Simple Notification Service) | SQS (Simple Queue Service) |
|---|---|---|
| Model | Publish/subscribe (push) | Queue (consumer pulls) |
| One message goes to | Every subscriber | One consumer |
| Stores messages | No. It delivers right away and retries delivery for a while. | Yes, up to 14 days, until a consumer deletes it. |
| If the receiver is down | Retries delivery, then drops the message (unless a DLQ is set on the subscription) | The message waits in the queue |
| Retries and dead-letter queue | Delivery retries, optional DLQ per subscription | Retries plus a dead-letter queue after N failed processing attempts |
| Good for | Spreading one event to many | Buffering work for one consumer at its own pace |

## When to use which

- **SNS** when one event has to reach several places. This is the fan-out part.
- **SQS** when a consumer must not lose messages, needs to work at its own speed, or needs retries and a dead-letter queue.

## Why use them together

SNS → SQS gives the best of both: SNS fans the event out, and each consumer gets its own queue. If one consumer is slow or broken, only its queue fills up. The other consumers and the main app are not affected, and no message is lost.
