# Event Flow

The current demo event carries identifiers only: `type`, `orderId` and `customerId`. It does not yet include the target design's `eventId`, amount or timestamp. See [notification-flow.md](../notifications/notification-flow.md).

```json
{
  "type": "order.shipped",
  "orderId": "A-2001",
  "customerId": "C-2001"
}
```

## When it works

1. The app publishes the event to the SNS topic.
2. SNS sends a copy to the email subscription and to the SQS queue.
3. Lambda reads from the queue and writes one log line, standing in for SMS and internal notifications.
4. The message is deleted from the queue.

## When it fails

1. Lambda throws an error.
2. The message comes back to the queue and is tried again.
3. After 3 failed tries it moves to the DLQ.
4. A CloudWatch alarm goes off.
5. The email already went out, so that part isn't affected.

The same message can arrive twice. Skipping duplicates by `eventId` is planned but not built.
