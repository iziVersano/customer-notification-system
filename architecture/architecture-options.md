# Architecture Options

In both options the app publishes to one SNS topic. The difference is what sits between SNS and the code.

## Option A: SNS → SQS → Lambda

```
App --> SNS --> email
         |
         +--> SQS --> Lambda --> logs
               |
               +--> DLQ (after 3 failed tries)
```

## Option B: SNS → Lambda

```
App --> SNS --> email
         |
         +--> Lambda --> logs
               |
               +--> DLQ (after Lambda's retries)
```

## Comparison

| | A (with SQS) | B (direct) |
|---|---|---|
| Consumer down | messages wait in the queue | no real buffer |
| Retries | I can configure them | 2 at most |
| See the backlog | queue depth in CloudWatch | no |
| Effort | a bit more Terraform | least |
| Cost | free tier | free tier |

## Decision

Option A. It costs almost nothing extra, messages survive when the consumer is down, and I can see and control the retries. B would be fine if losing an event now and then was OK, but here it isn't.
