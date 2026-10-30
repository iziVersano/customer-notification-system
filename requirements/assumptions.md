# Assumptions & Constraints

## Assumptions

- The main application is not part of this project. I simulate it by publishing test events from the AWS CLI or a small script.
- Real email is sent only to my own address. SMS and internal notifications are simulated: the Lambda writes them to the logs instead of sending them.
- Volume is low: tens to hundreds of events per day.
- A notification arriving a few seconds late is fine. It doesn't have to be instant.
- A customer getting the same notification twice now and then is acceptable, but should be avoided where it's easy.

## Constraints

- Four weeks, one person.
- My own AWS account, region `eu-central-1` (Frankfurt), free-tier budget.
- Infrastructure only through Terraform, no manual setup in the console for the final version.
- Only the services the problem needs: SNS, SQS, Lambda, CloudWatch, IAM.
- Everything is destroyed after the final demo.
