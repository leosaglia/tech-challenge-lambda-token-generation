terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "state-terraform-tech"
    key = "tech-challenge-lambda-token-generation/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}