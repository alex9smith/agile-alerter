# Agile alerter

Email you the next days' Octopus Agile prices every evening.

This is a serverless application that runs on AWS.

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

- eventbridge trigger
- pricing disclaimer
- application architecture
