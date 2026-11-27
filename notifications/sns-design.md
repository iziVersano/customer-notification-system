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
- **Encrypted at rest.** The `customer-events` topic uses AWS-managed `alias/aws/sns`; the `alerts` topic uses the customer-managed key in `terraform/encryption.tf` so CloudWatch can be granted `kms:Decrypt` and `kms:GenerateDataKey*`. The custom key policy allows the Terraform caller and SNS for the alerts topic, and CloudWatch use is scoped to the DLQ alarm. The CloudWatch SNS publish policy is also scoped to that alarm. The custom key has a cost and a 7-day deletion window.

Set up in `terraform/sns.tf` and `terraform/alarms.tf`.
