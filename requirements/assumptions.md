# Assumptions & Constraints

## Assumptions

- The course core has no main app. I simulate it by publishing test events from the CLI. A later extension adds a Django API.
- Real emails only go to me. SMS and internal notifications are just written to the logs.
- Low volume, up to a few hundred events a day.
- A few seconds of delay is fine.

## Constraints

- 4 weeks, working alone.
- My own AWS account, `eu-central-1`. The course core should stay within the free tier.
- Terraform only for the final setup.
- The course core uses SNS, SQS, Lambda, DynamoDB, CloudWatch and IAM.
- Extensions add EC2, a load balancer, Fargate, RDS, ECR, S3 and CloudFront. These cost money, so they only run during working sessions.
- Everything gets destroyed after the demo.
