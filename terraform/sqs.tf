resource "aws_sqs_queue" "notifications" {
  name = "notifications"

  # Long polling: a receive call waits up to 20 seconds for a message instead of returning empty.
  receive_wait_time_seconds = 20
  message_retention_seconds = 345600 # 4 days
}

# Only the customer-events topic may send to this queue.
data "aws_iam_policy_document" "notifications_queue" {
  statement {
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.notifications.arn]

    principals {
      type        = "Service"
      identifiers = ["sns.amazonaws.com"]
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_sns_topic.customer_events.arn]
    }
  }
}

resource "aws_sqs_queue_policy" "notifications" {
  queue_url = aws_sqs_queue.notifications.id
  policy    = data.aws_iam_policy_document.notifications_queue.json
}

# Raw delivery puts the event itself in the message body, without the SNS envelope.
resource "aws_sns_topic_subscription" "notifications_queue" {
  topic_arn            = aws_sns_topic.customer_events.arn
  protocol             = "sqs"
  endpoint             = aws_sqs_queue.notifications.arn
  raw_message_delivery = true
}
