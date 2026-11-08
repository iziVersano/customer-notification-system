resource "aws_sns_topic" "customer_events" {
  name = "customer-events"
}

# AWS sends a confirmation email. Nothing is delivered until the link in it is clicked.
resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.customer_events.arn
  protocol  = "email"
  endpoint  = var.notification_email
}
