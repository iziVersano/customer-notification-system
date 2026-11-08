variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "eu-central-1"
}

variable "aws_profile" {
  description = "AWS CLI profile used to run Terraform"
  type        = string
  default     = "dci"
}

variable "aws_account_id" {
  description = "The only AWS account Terraform may change"
  type        = string
  default     = "272423022449"
}

variable "notification_email" {
  description = "Address that receives the email notifications"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Name used in resource names and tags"
  type        = string
  default     = "customer-notification-system"
}
