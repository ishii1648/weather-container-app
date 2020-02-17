resource "aws_ecr_repository" "ecr_repository_01" {
  name                 = "weather-csv-api"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "ecr_repository_02" {
  name                 = "setup-db-job"
  image_tag_mutability = "MUTABLE"
}