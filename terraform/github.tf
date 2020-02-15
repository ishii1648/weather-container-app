provider "github" {
  organization = "ishii1648"
}

resource "github_repository_webhook" "repository_webhook" {
  repository = var.repo_name

  configuration {
      url           = aws_codepipeline_webhook.codepipeline_webhook.url
      secret        = var.secret_token
      content_type  = "json"
      insecure_ssl  = false
  }

  events = ["push"]
}
