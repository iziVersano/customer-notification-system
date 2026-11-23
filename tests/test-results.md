# Test Results

All tests ran against the deployed system in the DCI account (`eu-central-1`). Events are made up.

| # | Test | Date | Result |
|---|---|---|---|
| 1 | Account guard refuses any other account | 2026-11-13 | ✅ Pass |
| 2 | Happy path: event → SNS → email + SQS → Lambda log | 2026-11-13 | ✅ Pass |
| 3 | Failure path: bad event → 3 tries → DLQ → alarm | 2026-11-13 | ✅ Pass |
| 4 | Failure path up to the alert email | 2026-11-22 | ✅ Pass |

## 1. Account guard

Ran `terraform plan` with a wrong account id (`-var aws_account_id=111111111111`) while logged in to the DCI account.

```
Error: AWS account ID not allowed: 272423022449
```

Terraform stops before reading or changing anything, so the code can only ever touch the one allowed account.

## 2. Happy path

Published one valid event to the `customer-events` topic:

```json
{"type":"order.shipped","orderId":"A-1042","customer":"Lena Hoffmann","email":"lena@example.com","carrier":"DHL","shippedAt":"2026-11-13T09:15:00Z"}
```

- The email subscription delivered it to the inbox.
- The queue received it as the raw event (no SNS envelope).
- The Lambda logged it in CloudWatch (`/aws/lambda/notification-lambda`):

```
INFO {"level":"info","messageId":"5eecb4b8-…","type":"order.shipped","orderId":"A-1042","notify":"lena@example.com"}
Duration: 39.35 ms  Max Memory Used: 72 MB
```

## 3. Failure path

Published an event without an `email` field:

```json
{"type":"order.shipped","orderId":"A-1043","customer":"Test Broken"}
```

The Lambda rejects it and reports it as a failed batch item, so only this message goes back to the queue. It becomes visible again after the 30-second visibility timeout.

| Time (UTC) | What happened |
|---|---|
| 08:08:53 | Try 1: `event needs type, orderId and email` |
| 08:09:23 | Try 2: same error |
| 08:09:53 | Try 3: same error |
| 08:10:37 | `maxReceiveCount = 3` reached: the message is in `notifications-dlq` |
| 08:13:45 | Alarm `notifications-dlq-not-empty` changes to **ALARM** and notifies the `alerts` topic |

The good messages are not blocked while this one fails, and the bad one is kept for 14 days for a person to look at.

## 4. Alert email

Test 3 stopped at the topic. Its email subscription was never confirmed, so no email went out. I created it again, confirmed it, emptied the DLQ and published a bad event (`A-1044`).

| Time (UTC) | What happened |
|---|---|
| 12:12:52 | With the DLQ empty, the alarm changes to OK and the OK email arrives |
| 12:20:54 | Bad event published |
| 12:20:55 | Try 1 fails |
| 12:21:25 | Try 2 fails |
| 12:21:55 | Try 3 fails |
| about 12:22:30 | The message is in the DLQ |
| 12:25:52 | The alarm changes to ALARM and the email arrives in the inbox |
