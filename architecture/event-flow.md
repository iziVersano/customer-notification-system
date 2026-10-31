# Event Flow

Example event (only IDs and the amount, no personal data):

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

## When it works

1. The app publishes the event to the SNS topic.
2. SNS sends a copy to the email subscription and to the SQS queue.
3. Lambda reads from the queue and writes the SMS and internal notifications to the logs.
4. The message is deleted from the queue.

## When it fails

1. Lambda throws an error.
2. The message comes back to the queue and is tried again.
3. After 3 failed tries it moves to the DLQ.
4. A CloudWatch alarm goes off.
5. The email already went out, so that part isn't affected.

The same message can arrive twice, so Lambda uses `eventId` to skip duplicates (week 3).
