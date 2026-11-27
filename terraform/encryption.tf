data "aws_caller_identity" "current" {}

data "aws_iam_session_context" "current" {
  arn = data.aws_caller_identity.current.arn
}

# CloudWatch cannot use alias/aws/sns for the alarm topic because its key policy
# is AWS-managed and cannot grant CloudWatch the required KMS permissions.
resource "aws_kms_key" "sns_alerts" {
  description             = "Encrypt the SNS alerts topic"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnableIAMUserPermissions"
        Effect    = "Allow"
        Principal = { AWS = "arn:aws:iam::${var.aws_account_id}:root" }
        Action    = "kms:*"
        Resource  = "*"
      },
      {
        Sid       = "AllowTerraformPublisher"
        Effect    = "Allow"
        Principal = { AWS = data.aws_iam_session_context.current.issuer_arn }
        Action    = ["kms:Decrypt", "kms:GenerateDataKey*"]
        Resource  = "*"
        Condition = {
          StringEquals = {
            "kms:EncryptionContext:aws:sns:topicArn" = "arn:aws:sns:${var.aws_region}:${var.aws_account_id}:alerts"
          }
        }
      },
      {
        Sid       = "AllowSNSForAlertsTopic"
        Effect    = "Allow"
        Principal = { Service = "sns.amazonaws.com" }
        Action    = ["kms:Decrypt", "kms:GenerateDataKey*"]
        Resource  = "*"
        Condition = {
          StringEquals = {
            "kms:EncryptionContext:aws:sns:topicArn" = "arn:aws:sns:${var.aws_region}:${var.aws_account_id}:alerts"
          }
        }
      },
      {
        Sid       = "AllowCloudWatchAlarmToUseKey"
        Effect    = "Allow"
        Principal = { Service = "cloudwatch.amazonaws.com" }
        Action    = ["kms:Decrypt", "kms:GenerateDataKey*"]
        Resource  = "*"
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = var.aws_account_id
            "kms:EncryptionContext:aws:sns:topicArn" = "arn:aws:sns:${var.aws_region}:${var.aws_account_id}:alerts"
          }
          ArnEquals = {
            "aws:SourceArn" = "arn:aws:cloudwatch:${var.aws_region}:${var.aws_account_id}:alarm:notifications-dlq-not-empty"
          }
        }
      },
    ]
  })
}
