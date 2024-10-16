variable "email_addresses" {
  type        = list(string)
  description = "The email addresses to send pricing and budget alerts to"
}

variable "region" {
  type        = string
  default     = "C"
  description = "Which of Octopus' regions your want alerts for. Defaults to London"
}

variable "lambda_function_name" {
  default = "agile_alerter_lambda"
}

variable "resource_tags" {
  description = "Tags to apply to AWS resources"
  default = {
    Application = "agile-alerter"
  }
}