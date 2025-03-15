data "aws_vpc" "selected_vpc" {
  filter {
    name   = "tag:Name"
    values = ["tech-challenge-VPC"]
  }
}

data "aws_subnets" "private_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected_vpc.id]
  }

  filter {
    name   = "tag:Name"
    values = ["tech-challenge-PrivateSubnet1", "tech-challenge-PrivateSubnet2"]
  }

  depends_on = [data.aws_vpc.selected_vpc]
}

data "aws_iam_role" "role" {
  name = "LabRole"
}