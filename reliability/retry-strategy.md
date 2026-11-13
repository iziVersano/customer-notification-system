# Retry Strategy

Retries come from SQS itself, the Lambda doesn't loop.

When the Lambda gets a batch, it handles each message on its own. If one fails, it returns that message's id in `batchItemFailures`. Lambda deletes the messages that worked, and only the failed one goes back to the queue. One bad message doesn't make the whole batch run again.

The failed message becomes visible again after the visibility timeout (30 seconds), and the Lambda picks it up again. After 3 tries it goes to the DLQ.

Why 3: a temporary problem (a short outage, a timeout) usually passes within a minute. If it still fails after 3 tries, it is most likely bad data, and retrying more won't help.

The Lambda timeout is 10 seconds, below the 30-second visibility timeout, so a slow run can't make the same message show up twice at the same time.

Not done yet: duplicate checks. SQS can deliver the same message more than once, so the next step is to store each `eventId` in DynamoDB and skip ones already handled.
