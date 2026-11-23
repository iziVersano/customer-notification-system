# Cost Analysis

At demo volume I expect about $0 a month. These are estimates from AWS's list prices and free limits, not from a bill.

## Today

| Service | Free every month | What this project uses |
|---|---|---|
| SNS publishes | 1 million | A handful of test events |
| SNS email | 1,000 | A handful |
| SQS requests | 1 million | About 260,000, almost all empty polls |
| Lambda | 1 million calls and 400,000 GB-seconds | A handful of calls |
| CloudWatch Logs | 5 GB | Far below 1 MB, kept 7 days |
| CloudWatch alarms | 10 | 1 |
| AWS Budgets | Budgets with email alerts are free | 1 |

The one thing that runs all the time is polling. I measured about 8,600 empty receives a day on the queue (15–21 November). That is roughly 260,000 a month, with no events at all. 20-second long polling keeps it low.

## At a few hundred events a day

300 events a day is 9,000 emails a month, which is over the 1,000 free ones. The other 8,000 cost about $0.16. Everything else stays free.

## At 1 million events a month

A rough upper estimate, after the free limits:

| Part | Calculation | Per month |
|---|---|---|
| SNS publishes | Within 1 million free | $0 |
| SNS email, one subscriber | 999,000 at $2 per 100,000 | about $20 |
| SQS | Up to 3.3 million requests, 2.3 million paid at $0.40 per million | about $0.90 |
| Lambda | At most 1 million short calls at 128 MB | $0 |
| Logs | About 1 GB, within 5 GB free | $0 |
| **Total** | | **about $21** |

Email is almost all of it. SNS doesn't charge per delivery to SQS, only for data transfer, which is small with events this size.

## Keeping it cheap

- A $5 monthly budget emails at $4 actual spend and when the forecast goes over $5.
- No servers, NAT gateway or database in AWS.
- `terraform destroy` after the presentation.
