resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = "weather-container-app-pipeline-bucket"
  force_destroy = true
  acl    = "private"
}

resource "aws_codepipeline" "codepipeline" {
  name     = "${var.project_name}-pipeline"
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = aws_s3_bucket.codepipeline_bucket.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        Owner               = var.repo_owner
        Repo                = var.repo_name
        Branch              = var.repo_branch
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      version          = "1"

      configuration = {
        ProjectName = aws_codebuild_project.codebuild.name
      }
    }
  }
}

resource "aws_codepipeline_webhook" "codepipeline_webhook" {
  name            = "${var.project_name}-pipeline-webhook"
  target_pipeline = aws_codepipeline.codepipeline.name
  target_action   = "Source"
  authentication  = "GITHUB_HMAC"

  authentication_configuration {
    secret_token = var.secret_token
  }

  filter {
    json_path    = "$.ref"
    match_equals = "refs/heads/{Branch}"
  }
}
