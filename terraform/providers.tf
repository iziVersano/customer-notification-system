provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile

  # Stops every plan and apply if the credentials belong to any other account.
  allowed_account_ids = [var.aws_account_id]

  default_tags {
    tags = {
      Project   = var.project_name
      ManagedBy = "terraform"
    }
  }
}
