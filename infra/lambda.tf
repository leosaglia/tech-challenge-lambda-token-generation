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
    security_group_ids = ["sg-05efd16d50f3f107e"]
  }
}