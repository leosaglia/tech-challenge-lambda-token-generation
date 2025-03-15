resource "aws_security_group" "lambda_sg" {
  name        = "lambda-token-generation-sg"
  description = "Security group for lambda function"
  vpc_id      = data.aws_vpc.selected_vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "archive_file" "lambda_package" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_lambda_function" "lambda" {
  function_name    = "tech-challenge-customer-token-generation"
  filename         = data.archive_file.lambda_package.output_path
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  role             = data.aws_iam_role.role.arn
  source_code_hash = filebase64sha256(data.archive_file.lambda_package.output_path)
  
  vpc_config {
    subnet_ids         = [for id in data.aws_subnets.private_subnets.ids : id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      NLB_BASE_URL = "http://af1d21e4bcb6e4e0098954d613411cda-e935e40cf52b0a60.elb.us-east-1.amazonaws.com:3001"
    }
  }
}