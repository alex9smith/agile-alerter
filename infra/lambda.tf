resource "aws_lambda_function" "agile_alerter_lambda" {
  function_name    = var.lambda_function_name
  filename         = "lambda_function_payload.zip"
  role             = aws_iam_role.agile_alerter_lambda_role.arn
  handler          = "lambda.handler"
  layers           = [aws_lambda_layer_version.requirements_layer.arn]
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime          = "python3.12"
  architectures    = ["arm64"]
  timeout          = 5
  tags             = var.resource_tags

  environment {
    variables = {
      REGION    = var.region,
      TOPIC_ARN = aws_sns_topic.pricing_alerts.arn
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.example,
  ]
}

data "archive_file" "lambda" {
  type        = "zip"
  source_dir  = "../app"
  output_path = "lambda_function_payload.zip"
}

resource "null_resource" "pip_install" {
  triggers = {
    shell_hash = "${sha256(file("../requirements.txt"))}"
  }

  provisioner "local-exec" {
    command = "python3 -m pip install -r ../requirements.txt -t ../app/layer/python"
  }
}

data "archive_file" "requirements_layer" {
  type        = "zip"
  source_dir  = "../app/layer"
  output_path = "../app/layer.zip"
  depends_on  = [null_resource.pip_install]
}

resource "aws_lambda_layer_version" "requirements_layer" {
  layer_name          = "requirements_layer"
  filename            = data.archive_file.requirements_layer.output_path
  source_code_hash    = data.archive_file.requirements_layer.output_base64sha256
  compatible_runtimes = ["python3.12"]
}


data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "agile_alerter_lambda_role" {
  name               = "agile_alerter_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  tags               = var.resource_tags
}

resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 7
  tags              = var.resource_tags
}

data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json
  tags        = var.resource_tags
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.agile_alerter_lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

data "aws_iam_policy_document" "publish_to_sns" {
  statement {
    effect    = "Allow"
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.pricing_alerts.arn]
  }
}

resource "aws_iam_policy" "agile_alerter_publish_to_sns" {
  name        = "agile_alerter_publish_to_sns"
  path        = "/"
  description = "Allow the lambda to publish to the SNS topic"
  policy      = data.aws_iam_policy_document.publish_to_sns.json
  tags        = var.resource_tags
}

resource "aws_iam_role_policy_attachment" "publish_to_sns" {
  role       = aws_iam_role.agile_alerter_lambda_role.name
  policy_arn = aws_iam_policy.agile_alerter_publish_to_sns.arn
}