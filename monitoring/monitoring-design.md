# Monitoring Design

What we watch right now:

**Lambda logs.** Every event the Lambda handles writes one JSON line to CloudWatch Logs (`/aws/lambda/notification-lambda`), with the message id, event type and order id. Failures are logged as `error` with the reason. Logs are kept 7 days.

**DLQ alarm.** `notifications-dlq-not-empty` checks the DLQ every minute. If there is at least one message, it goes to ALARM and sends an email through the `alerts` SNS topic. It sends another one when the DLQ is empty again. In the failure test it fired about 3 minutes after the message reached the DLQ.

The alerts have their own topic so they don't mix with customer events.

**Cost.** A $5 monthly budget emails at $4 actual spend and when the forecast goes over $5.

Later, if needed: an alarm on Lambda errors, and one on the age of the oldest message in the main queue (to see if processing falls behind).

Set up in `terraform/alarms.tf` and `terraform/budget.tf`.
