# Assumptions & Constraints

## Assumptions

- The main app isn't part of this project. I simulate it by publishing test events from the CLI.
- Real emails only go to me. SMS and internal notifications are just written to the logs.
- Low volume, up to a few hundred events a day.
- A few seconds of delay is fine.

## Constraints

- 4 weeks, working alone.
- My own AWS account, `eu-central-1`, free tier.
- Terraform only for the final setup.
- Only SNS, SQS, Lambda, CloudWatch and IAM.
- Everything gets destroyed after the demo.
