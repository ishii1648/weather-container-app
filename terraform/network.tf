module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.cluster_name}"
  cidr = "10.0.0.0/16"

  azs             = ["ap-northeast-1d", "ap-northeast-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway                = true
  enable_dns_hostnames              = true
  default_vpc_enable_dns_hostnames  = true

  tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}

resource "aws_security_group" "ingress" {
  name_prefix = "ingress"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }
}

resource "aws_security_group" "app" {
  name_prefix = "app"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 1025
    to_port   = 65535
    protocol  = "tcp"

    security_groups = [aws_security_group.ingress.id]
  }
}
