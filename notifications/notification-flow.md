# Notification Flow

What happens to one event, as it runs today.

## A good event

```json
{"type":"order.shipped","orderId":"A-1042","customerId":"C-1042"}
```

1. I publish it to `customer-events`, playing the app.
2. SNS sends it to my inbox and puts a copy in the `notifications` queue.
3. The Lambda checks that `type`, `orderId` and `customerId` are there.
4. It writes one log line. This stands in for sending an SMS or an internal message.
5. The message is deleted from the queue.

## A bad event

The same event without `customerId`:

| About when | What happens |
|---|---|
| 0:00 | Published. The email subscriber still gets it, because SNS doesn't check content |
| 0:01 | The Lambda's first try fails |
| 0:31 | Second try fails |
| 1:01 | Third try fails |
| 1:35 | The message is in the DLQ |
| 5:00 | The alarm turns on and emails me |

Most of the last wait is CloudWatch: SQS metrics reach it with a delay.

Afterwards a person fixes the cause and redrives the message, or deletes it. When the DLQ is empty the alarm goes back to OK and emails again.

Historical tests used synthetic names and email addresses. Current demo events carry IDs only.
