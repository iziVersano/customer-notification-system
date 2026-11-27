# Demo Script

Monday 23 November, 10:10–10:30. About 5 minutes of slides and demo (the limit is 10), then questions.

## Reset after every rehearsal

The alarm only emails when it changes from OK to ALARM. If an old message is still in the DLQ, the demo sends no email. So after each run:

```bash
aws sqs purge-queue --profile dci --region eu-central-1 --queue-url https://sqs.eu-central-1.amazonaws.com/272423022449/notifications-dlq
```

Wait until this prints `OK` (about 3 to 5 minutes):

```bash
aws cloudwatch describe-alarms --profile dci --region eu-central-1 --alarm-names notifications-dlq-not-empty --query 'MetricAlarms[0].StateValue' --output text
```

## Before you speak

By 09:45:

- The alarm prints `OK`.
- Open `slides.pdf`, Gmail and a terminal with a big font. Close everything else.
- Have the backup recording ready.

At 10:00, publish the bad event (it has no customerId field). It needs about 5 minutes to reach the alarm.

```bash
aws sns publish --profile dci --region eu-central-1 --topic-arn arn:aws:sns:eu-central-1:272423022449:customer-events --message '{"type":"order.shipped","orderId":"A-2002"}'
```

When rehearsing, publish it 10 minutes before you start the timer.

## 0:00 Slide 1: the problem

> Hi, I'm Izi. I built a notification system for NotifyNow. Their app sends every notification itself, so one broken channel can break an order.
>
> With an event-driven design, the app only says "this happened".

## 0:25 Slide 2: how it works

> The app publishes one event to SNS, which copies it to email and to an SQS queue. That's fan-out.
>
> The queue holds work during bursts or short problems, and Lambda scales to process it.
>
> After three failed tries, a message moves to the dead-letter queue and CloudWatch emails me.

## 1:15 Slide 3: review and next steps

> I reviewed it against the six Well-Architected pillars. Each part has limited permissions, Terraform builds it all, and it costs about zero at this volume.
>
> Next I would add a duplicate check, use IDs only in events, encrypt SNS and automate deploys.

## 2:00 Demo: it works

> I'll publish one good event.

```bash
aws sns publish --profile dci --region eu-central-1 --topic-arn arn:aws:sns:eu-central-1:272423022449:customer-events --message '{"type":"order.shipped","orderId":"A-2001","customerId":"C-2001"}'
```

Show the email in Gmail, then the log:

```bash
aws logs tail /aws/lambda/notification-lambda --profile dci --region eu-central-1 --since 20m --format short
```

> One event, two receivers: the email and the Lambda log.

## 3:15 Demo: it fails safely

> Earlier I sent a broken event.

Point at the three errors in the log, then show the DLQ and the alarm email:

```bash
aws sqs get-queue-attributes --profile dci --region eu-central-1 --queue-url https://sqs.eu-central-1.amazonaws.com/272423022449/notifications-dlq --attribute-names ApproximateNumberOfMessages
```

> Three tries, then it was set aside and I got an email.

## 4:30 Close

> Thank you, I'm happy to take questions.

## If something breaks

- No internet or an AWS error: play the recording and keep talking.
- An email is late: show the log or the alarm state, and come back to the inbox in the questions.
- Don't run `terraform destroy` until the questions are over.
