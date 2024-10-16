data "aws_iam_policy_document" "scheduler_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "scheduler_role" {
  name               = "eventbridge_scheduler_role"
  assume_role_policy = data.aws_iam_policy_document.scheduler_assume_role.json
}

data "aws_iam_policy_document" "eventbridge_invoke_policy" {
  statement {
    effect = "Allow"
    actions = [
      "lambda:InvokeFunction"
    ]
    resources = [aws_lambda_function.agile_alerter_lambda.arn]
  }
}

resource "aws_iam_role_policy" "eventbridge_invoke_policy" {
  name   = "eventbridge_invoke_lambda_policy"
  role   = aws_iam_role.scheduler_role.id
  policy = data.aws_iam_policy_document.eventbridge_invoke_policy.json
}

resource "aws_scheduler_schedule" "agile_alerter_schedule" {
  name = "agile_alerter_schedule"

  flexible_time_window {
    mode = "OFF"
  }

  # Every day at 9PM
  schedule_expression = "cron(0 19 * * ? *)"

  target {
    arn      = aws_lambda_function.agile_alerter_lambda.arn
    role_arn = aws_iam_role.scheduler_role.arn
  }

}