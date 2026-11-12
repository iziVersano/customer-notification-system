# The built handler (npm run build in lambda/) zipped for upload.
data "archive_file" "notification_lambda" {
  type        = "zip"
  source_file = "${path.module}/../lambda/dist/index.mjs"
  output_path = "${path.module}/build/notification-lambda.zip"
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "notification_lambda" {
  name               = "notification-lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

# Least privilege: read only this queue and write only this function's logs.
data "aws_iam_policy_document" "notification_lambda" {
  statement {
    actions   = ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
    resources = [aws_sqs_queue.notifications.arn]
  }

  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["${aws_cloudwatch_log_group.notification_lambda.arn}:*"]
  }
}

resource "aws_iam_role_policy" "notification_lambda" {
  name   = "read-queue-write-logs"
  role   = aws_iam_role.notification_lambda.id
  policy = data.aws_iam_policy_document.notification_lambda.json
}

# Created by Terraform so the retention is set; Lambda would otherwise make one that keeps logs forever.
resource "aws_cloudwatch_log_group" "notification_lambda" {
  name              = "/aws/lambda/notification-lambda"
  retention_in_days = 7
}

resource "aws_lambda_function" "notification" {
  function_name    = "notification-lambda"
  role             = aws_iam_role.notification_lambda.arn
  runtime          = "nodejs22.x"
  handler          = "index.handler"
  filename         = data.archive_file.notification_lambda.output_path
  source_code_hash = data.archive_file.notification_lambda.output_base64sha256
  timeout          = 10
  memory_size      = 128

  depends_on = [aws_iam_role_policy.notification_lambda, aws_cloudwatch_log_group.notification_lambda]
}

# AWS polls the queue for the function and passes up to 10 messages per call.
# ReportBatchItemFailures: only the messages the handler lists as failed return to the queue.
resource "aws_lambda_event_source_mapping" "notifications_queue" {
  event_source_arn        = aws_sqs_queue.notifications.arn
  function_name           = aws_lambda_function.notification.arn
  batch_size              = 10
  function_response_types = ["ReportBatchItemFailures"]
}
