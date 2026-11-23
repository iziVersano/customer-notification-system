# SNS Design

There are two topics, so alerts don't mix with customer events.

| Topic | Who publishes | Who receives |
|---|---|---|
| `customer-events` | The app (me, from the CLI) | My email and the `notifications` queue |
| `alerts` | The CloudWatch DLQ alarm | My email |

## customer-events

- A standard topic. Order doesn't matter here, and FIFO topics can't send email.
- No filters, so both subscribers get every event, broken ones too.
- The queue subscription uses raw delivery, so the Lambda gets the event itself without the SNS envelope.

## Things to know

- **Email has to be confirmed.** Until someone clicks the link, SNS sends nothing. My first `alerts` subscription was never confirmed and disappeared, so the alarm emailed nobody. Fixed and tested on 22 November.
- **Email goes to a fixed list.** It can't send to the customer named in the event, and the mail is plain JSON. Real customer email needs a consumer that uses SES.
- **SNS doesn't keep messages for later.** If a delivery fails on the AWS side it retries, up to 23 days for SQS and 6 hours for email, and then drops the message. There is no DLQ on the subscriptions.
- **Not encrypted at rest yet.** See [iam-design.md](../security/iam-design.md).

Set up in `terraform/sns.tf` and `terraform/alarms.tf`.
