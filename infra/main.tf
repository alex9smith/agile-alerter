terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  required_version = ">= 1.9.0"
}

provider "aws" {
  region = "eu-west-2"
}