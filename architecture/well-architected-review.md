# Well-Architected Review

My own check of the project against the six pillars, on 22 November 2026.

| Pillar | In place | Gap | Next step |
|---|---|---|---|
| Operational excellence | Terraform, CI checks, logs, tested alarm | Deploys are manual, state is local | OIDC deploys, state in S3 |
| Security | Least privilege, account guard, queue policy, SQS encrypted | SNS not encrypted; IDs-only event schema now in place | Encrypt SNS |
| Reliability | Queue, 3 tries, DLQ, failures reported per message | Duplicates aren't detected, short visibility timeout, no DLQ on subscriptions | DynamoDB check, 60-second timeout, subscription DLQs |
| Performance efficiency | Serverless, batches of up to 10 | No load test | Send a burst and watch the queue age |
| Cost optimization | Free-tier services, long polling, $5 budget | Email costs above 1,000 a month | Compare SES before real volume |
| Sustainability | No servers, logs deleted after 7 days | Not measured | Try arm64 for the Lambda |

## What I would fix first

1. The duplicate check, because SQS will deliver something twice sooner or later.
2. Encrypt SNS.
