output "customer_events_topic_arn" {
  description = "Topic the app publishes events to"
  value       = aws_sns_topic.customer_events.arn
}
