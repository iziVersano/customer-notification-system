output "customer_events_topic_arn" {
  description = "Topic the app publishes events to"
  value       = aws_sns_topic.customer_events.arn
}

output "notifications_queue_url" {
  description = "Queue the Lambda reads from"
  value       = aws_sqs_queue.notifications.id
}

output "notifications_queue_arn" {
  description = "ARN of the notifications queue"
  value       = aws_sqs_queue.notifications.arn
}
