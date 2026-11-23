# Assumptions & Constraints

## Assumptions

- The course core has no main app. I simulate it with the small demo page in `demo-ui/`, or by publishing test events from the CLI.
- Real emails only go to me. One log line per event stands in for SMS and internal notifications.
- Low volume, up to a few hundred events a day.
- A few seconds of delay is fine.

## Constraints

- 4 weeks, working alone.
- My own AWS account, `eu-central-1`. The course core should stay within the free tier.
- Terraform only for the final setup.
- The course core uses SNS, SQS, Lambda, CloudWatch, IAM and Budgets. DynamoDB was planned for duplicate checks and isn't built.
- Planned extensions, none deployed, would add EC2, a load balancer, Fargate, RDS, ECR, S3 and CloudFront. These cost money, so they only run during working sessions.
- Everything gets destroyed after the demo.
