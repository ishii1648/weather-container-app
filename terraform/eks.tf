data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token                  = data.aws_eks_cluster_auth.cluster.token
  version                = "~> 1.9"
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name 
  cluster_version = "1.14"
  subnets         = concat(module.vpc.public_subnets, module.vpc.private_subnets)
  vpc_id          = module.vpc.vpc_id

  worker_groups_launch_template = [
    {
      name = "nginx-ingress"

      override_instance_types = ["t3.small"]
      spot_instance_pools     = 1
      asg_max_size            = 2
      kubelet_extra_args      = "--node-labels=kubernetes.io/lifecycle=spot,tier=front-end"
      subnets                 = module.vpc.public_subnets
      public_ip               = true
      root_volume_size        = 10

      additional_security_group_ids = [aws_security_group.ingress.id]
    },
    {
      name = "app"

      override_instance_types = ["t3.small"]
      spot_instance_pools     = 1
      asg_max_size            = 2
      kubelet_extra_args      = "--node-labels=kubernetes.io/lifecycle=spot,tier=back-end"
      subnets                 = module.vpc.private_subnets
      root_volume_size        = 10

      additional_security_group_ids = [aws_security_group.app.id]
    }
  ]
}
