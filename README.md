# Customer Notification System

DCI Cloud final project. The app publishes an event once, and AWS passes it on to several notification consumers.

## Project Overview

![Architecture](architecture/architecture-diagram.png)

App → SNS → email and SQS → Lambda. Messages that keep failing go to a dead-letter queue. CloudWatch has the logs and alarms.

## Business Problem

NotifyNow's app sends every email, SMS and internal message itself, so a broken channel can break the app, and each new notification type means changing the app. More in [architecture/current-architecture.md](architecture/current-architecture.md).

## Requirements

See [requirements/](requirements/).

## Architecture Options

See [architecture/architecture-options.md](architecture/architecture-options.md).

## Final Architecture

Option A: SNS → SQS → Lambda.

1. An event is published to the `customer-events` topic. There is no app yet, so I publish from the CLI.
2. SNS sends it to an email subscriber and to the `notifications` queue.
3. A TypeScript Lambda reads the queue, checks the event and logs it.
4. After 3 failed tries a message moves to `notifications-dlq`.
5. A CloudWatch alarm on the DLQ emails me through the `alerts` topic.

The details are in [notifications/notification-flow.md](notifications/notification-flow.md).

## AWS Services

| Service | Used for |
|---|---|
| SNS | `customer-events` fan-out, and `alerts` for the alarm email |
| SQS | The `notifications` queue and its dead-letter queue |
| Lambda | Checks and logs each event (TypeScript, Node 22) |
| CloudWatch | Lambda logs and the DLQ alarm |
| IAM | The Lambda's least-privilege role |
| AWS Budgets | Email alert on a $5 monthly budget |

## Architecture Decisions

See [architecture/architecture-decisions.md](architecture/architecture-decisions.md).

## Terraform

Infrastructure lives in [terraform/](terraform/). Every command uses the `dci` AWS profile. Build the Lambda first, because Terraform zips the built file:

```bash
(cd lambda && npm ci && npm run build)
cd terraform
terraform init
terraform plan
```

## Testing

See [tests/test-results.md](tests/test-results.md).

## Well-Architected Review

See [architecture/well-architected-review.md](architecture/well-architected-review.md).

## Security

See [security/iam-design.md](security/iam-design.md).

## Cost Considerations

See [cost/cost-analysis.md](cost/cost-analysis.md).

## Limitations & Future Improvements

Not built or not finished:

- **Personal data.** Test events carry a made-up name and email, and the Lambda logs the email. The requirement says IDs only, so that isn't met yet.
- **Duplicates.** A repeated message is handled again. Next: a DynamoDB check on `eventId`, which the events also need to start sending.
- **Customer email and SMS.** SNS email goes to a fixed list, and SMS and internal messages are only stood in for by a log line. Next: consumers that really send, for example with SES.
- **Delivery overview.** The logs show what the Lambda handled, not whether an email was delivered.
- **Encryption.** The SNS topics aren't encrypted at rest.
- **Deploys.** CI only checks. Next: deploys with OIDC and remote Terraform state.
- **Backend.** `backend/` is an unfinished extension: a local Django skeleton with a health check and job models. It doesn't publish to SNS and isn't deployed.
- **Later:** Lamp to EU, product compliance checks on the same event system.

## Presentation

See [presentation/](presentation/).

## Cleanup

```bash
cd terraform
terraform destroy
```
