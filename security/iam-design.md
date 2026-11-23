# IAM and Security

The idea is simple: every part gets only the access it needs, and nothing more.

## Who can do what

| Who | Can do | Only on | Where |
|---|---|---|---|
| Lambda role `notification-lambda` | Read and delete messages, read queue attributes | The `notifications` queue | `terraform/lambda.tf` |
| Lambda role `notification-lambda` | Write log lines | Its own log group `/aws/lambda/notification-lambda` | `terraform/lambda.tf` |
| SNS | Send messages to the queue | Only when they come from the `customer-events` topic | `terraform/sqs.tf` (queue policy) |
| GitHub Actions | Read the repo | Nothing in AWS | `.github/workflows/checks.yml` |

The Lambda can't publish to SNS, can't read other queues, and can't touch any other log group. If someone breaks into the function, that is all they get.

The queue policy checks `aws:SourceArn`. "SNS may send" alone would let any SNS topic in any account send messages into our queue. With the check, only our topic can.

## Account guard

The AWS provider has `allowed_account_ids = [272423022449]`. If the credentials belong to any other account, Terraform stops before it reads or changes anything. Tested: see `tests/test-results.md`, test 1.

## Secrets

- No AWS keys in the repo. Terraform and the AWS CLI use the `dci` profile from `~/.aws`.
- `terraform.tfvars` holds my email and stays local. Only `example.tfvars` is committed.
- Terraform state stays on my machine. `*.tfstate` and plan files are in `.gitignore`, because state can contain real values.

## Encryption

- The SQS queue and the DLQ are encrypted at rest with SSE-SQS. AWS turns it on by default, and I checked it on the live queue.
- The SNS topics are not encrypted yet. The fix is one line per topic: `kms_master_key_id = "alias/aws/sns"`.
- Everything in transit uses HTTPS. The AWS APIs only accept TLS.

## Not done yet

- **IDs only.** Test events carry a made-up name and email, and the email ends up in the Lambda log.
- **SNS encryption**, as above.
- **OIDC for deploys.** A GitHub Actions role that only the repo's `main` branch can assume. Then no long-lived keys are needed in GitHub.
- **Remote state.** S3 with locking, so state isn't only on one laptop.
