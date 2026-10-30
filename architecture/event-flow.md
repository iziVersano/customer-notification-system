# Event Flow

## Example event

```json
{
  "eventType": "OrderCreated",
  "eventId": "evt-7f3a",
  "customerId": "12345",
  "orderId": "ORD-1001",
  "amount": 79.99,
  "currency": "EUR",
  "timestamp": "2026-10-30T10:15:00Z"
}
```

Only IDs and the amount. No names, emails or card data in the message.

## Happy path

1. The app publishes the event once to the SNS topic `customer-events`.
2. SNS copies it to every subscriber (fan-out):
   - the **email subscription** sends a short email to my inbox
   - the **SQS queue** `notifications` stores a copy
3. Lambda picks the message up from the queue.
4. Lambda builds the notification (SMS and internal, simulated) and writes it to CloudWatch Logs.
5. Lambda succeeds, so the message is deleted from the queue.

## Failure path

1. Lambda throws an error while processing.
2. The message becomes visible in the queue again after the visibility timeout and is retried.
3. After 3 failed tries it moves to the dead-letter queue `notifications-dlq`.
4. A CloudWatch alarm fires when the DLQ has messages.
5. The email subscriber is not affected and has already sent its email.

## Why `eventId`

The same message can be delivered more than once. Lambda uses `eventId` to recognise a duplicate and skip it (idempotency, week 3).
