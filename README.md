# Agile alerter

Email you the next days' Octopus Agile prices every evening.

This is a serverless application that runs on AWS.
It uses AWS EventBridge Scheduler to trigger a Lambda function at 8PM every day.
This Lambda calls the Octopus API to get pricing for the next day and sends the message to SNS.
The user's email is subscribed to the SNS topic to deliver the alert.

At time of writing (Oct 2024) all resource usage from this application falls within the AWS free tier but this may change at any point.
I am not liable for any costs you may incur from using this application.

To help prevent excessive costs, this application also deploys a budget alert for when total spend in a month exceeds $10.

## How to deploy

### Requirements

- Python
- Terraform
- AWS CLI with appropriate credentials configured

### Instructions

Switch to the `infra` directory

```bash
cd infra
```

Copy `example.tfvars` to `production.auto.tfvars`

```bash
cp example.tfvars production.auto.tfvars
```

Then fill in the variables with your email address and account region.

Now you're ready to run Terraform

```bash
terraform init
terraform apply
```

The application subscribes the provided email to an SNS topic.
Once deployed you'll be emailed a confirmation link.
You must click this link before you receive any emails.

## Developing

```bash
source venv/bin/activate
```

## TODO

- Make the budget alert optional
- Tag all resources
- Make the budget alert filter by tag
- Allow users to select other Agile tariffs
