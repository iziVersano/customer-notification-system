# Dead-Letter Queue

Some messages will never work, for example an event with no email address. Without a DLQ the Lambda would keep failing on it until the queue's 4 days run out, and nobody would know.

So the `notifications` queue has a dead-letter queue, `notifications-dlq`. After a message has been received 3 times without success, SQS moves it there.

- `maxReceiveCount = 3` on the main queue
- The DLQ keeps messages for 14 days, longer than the main queue, so there is time to look at them
- An alarm fires as soon as one message is in it (see `monitoring/monitoring-design.md`)

When something lands in the DLQ: read the message, fix the cause (bad data or a bug), then send it back to the main queue with SQS "redrive", or delete it.

Set up in `terraform/sqs.tf`.
