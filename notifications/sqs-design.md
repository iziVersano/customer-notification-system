# SQS Design

| Setting | `notifications` | `notifications-dlq` | Why |
|---|---|---|---|
| Type | Standard | Standard | Order doesn't matter |
| Retention | 4 days | 14 days | Time to look at failures |
| Long polling | 20 seconds | Default | Fewer empty requests |
| Visibility timeout | 30 seconds (default) | Default | Longer than the Lambda's 10 seconds |
| Max receives | 3, then to the DLQ | None | No endless retries |
| Encryption | SSE-SQS | SSE-SQS | On by default |

For standard queues the 14 days count from when the message first entered the main queue.

## Who can use it

- Only the `customer-events` topic can send to the main queue (queue policy with `aws:SourceArn`).
- The Lambda role can only read and delete from the main queue.

## How the Lambda reads it

AWS polls the queue and passes up to 10 messages per call. The Lambda returns the ones that failed, and only those come back.

## Known limits

- A standard queue delivers at least once, so duplicates can happen. They aren't detected yet.
- A throttled or failing Lambda also uses up the 3 receives. AWS recommends a visibility timeout of at least 6 times the function timeout, which would be 60 seconds here. That is a change for later.

Set up in `terraform/sqs.tf` and `terraform/lambda.tf`.
