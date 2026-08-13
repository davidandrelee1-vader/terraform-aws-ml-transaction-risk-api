resource "aws_iam_role" "lambda_execution" {
  name = "${lower(var.project_name)}-lambda-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Name    = "terraform-ml-lambda-execution"
    project = var.project_name
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "inference_api" {
  function_name = "${lower(var.project_name)}-inference-api"
  role          = aws_iam_role.lambda_execution.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.inference.repository_url}:lambda-v4"

  architectures = ["x86_64"]
  memory_size   = 1024
  timeout       = 30


  environment {
    variables = {
      PORT                         = "8000"
      AWS_LWA_PORT                 = "8000"
      AWS_LWA_READINESS_CHECK_PATH = "/health"
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic
  ]

  tags = {
    Name    = "terraform-ml-inference-api"
    project = var.project_name
  }
}

resource "aws_lambda_function_url" "inference_api" {
  function_name      = aws_lambda_function.inference_api.function_name
  authorization_type = "NONE"
  invoke_mode        = "BUFFERED"

  cors {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST"]
    allow_headers = ["content-type"]
    max_age       = 300
  }
}

resource "aws_lambda_permission" "public_url" {
  statement_id           = "AllowPublicFunctionURL"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.inference_api.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}

resource "aws_lambda_permission" "public_invoke" {
  statement_id             = "AllowPublicInvokeViaFunctionURL"
  action                   = "lambda:InvokeFunction"
  function_name            = aws_lambda_function.inference_api.function_name
  principal                = "*"
  invoked_via_function_url = true
}

output "inference_api_url" {
  description = "Public URL for the ML inference API"
  value       = aws_lambda_function_url.inference_api.function_url
}
