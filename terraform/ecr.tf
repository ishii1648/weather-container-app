resource "aws_ecr_repository" "ecr_repository" {
  name                 = "wheather-container-app"
  image_tag_mutability = "MUTABLE"
}