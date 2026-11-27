# Operational alerts go to their own topic, apart from the customer events.
resource "aws_sns_topic" "alerts" {
  name              = "alerts"
  kms_master_key_id = aws_kms_key.sns_alerts.arn
}

# Allow only this account's DLQ alarm to publish to the alerts topic.
data "aws_iam_policy_document" "alerts" {
  statement {
    sid       = "AllowAccountOwner"
    effect    = "Allow"
    actions   = ["SNS:*"]
    resources = [aws_sns_topic.alerts.arn]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.aws_account_id}:root"]
    }
  }

  statement {
    sid       = "AllowCloudWatchAlarmPublish"
    effect    = "Allow"
    actions   = ["SNS:Publish"]
    resources = [aws_sns_topic.alerts.arn]

    principals {
      type        = "Service"
      identifiers = ["cloudwatch.amazonaws.com"]
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = ["arn:aws:cloudwatch:${var.aws_region}:${var.aws_account_id}:alarm:notifications-dlq-not-empty"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [var.aws_account_id]
    }
  }
}

resource "aws_sns_topic_policy" "alerts" {
  arn    = aws_sns_topic.alerts.arn
  policy = data.aws_iam_policy_document.alerts.json
}

resource "aws_sns_topic_subscription" "alerts_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# Fires as soon as one message sits in the dead-letter queue.
resource "aws_cloudwatch_metric_alarm" "dlq_not_empty" {
  alarm_name          = "notifications-dlq-not-empty"
  alarm_description   = "A notification failed 3 times and is waiting in the dead-letter queue."
  namespace           = "AWS/SQS"
  metric_name         = "ApproximateNumberOfMessagesVisible"
  dimensions          = { QueueName = aws_sqs_queue.notifications_dlq.name }
  statistic           = "Maximum"
  period              = 60
  evaluation_periods  = 1
  threshold           = 0
  comparison_operator = "GreaterThanThreshold"
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  ok_actions          = [aws_sns_topic.alerts.arn]
}
