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

_TODO_

## AWS Services

_TODO_

## Architecture Decisions

See [architecture/architecture-decisions.md](architecture/architecture-decisions.md).

## Terraform

Infrastructure lives in [terraform/](terraform/). Every command uses the `dci` AWS profile:

```bash
cd terraform
terraform init
terraform plan
```

## Testing

See [tests/test-results.md](tests/test-results.md).

## Security

See [security/iam-design.md](security/iam-design.md).

## Cost Considerations

See [cost/cost-analysis.md](cost/cost-analysis.md).

## Limitations & Future Improvements

_TODO_

## Cleanup

```bash
cd terraform
terraform destroy
```
