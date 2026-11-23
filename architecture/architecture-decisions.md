# Architecture Decisions

The main choices, why I made them, and what each one costs me.

| # | Decision | Why | Downside |
|---|---|---|---|
| 1 | SNS topic as the only entry point | The app publishes once and doesn't know who listens | Every subscriber gets every event until I add filters |
| 2 | SQS between SNS and Lambda | Messages are stored, I control the retries, I can see the backlog | One more part, and messages can arrive twice |
| 3 | Lambda, no servers | Nothing to patch, nothing to pay for when idle | 15 minutes maximum per run, so long jobs would need something else |
| 4 | 3 tries, then a dead-letter queue | Bad data doesn't retry forever | An outage longer than about 90 seconds can fill the DLQ, which then needs a redrive |
| 5 | Report failures per message | One bad message doesn't repeat the whole batch | A little more code |
| 6 | A separate `alerts` topic | Alerts don't mix with customer events | A second subscription to confirm |
| 7 | Email through an SNS subscription | No code needed to show fan-out | It mails a fixed list, so it can't write to each customer. That needs a consumer with SES |
| 8 | Terraform with an account guard | Repeatable, and it can't hit the wrong account | State is only on my laptop for now |
| 9 | CI only checks, it doesn't deploy | No AWS access needed in GitHub | I deploy by hand |

## Put off

- **Duplicate check in DynamoDB.** It was planned for week 3 and isn't built.
- **Deploys with OIDC.** Also planned, not built.

The two options I compared first are in [architecture-options.md](architecture-options.md).
