resource "aws_sns_topic" "pricing_alerts" {
  name = "pricing_alerts_topic"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.pricing_alerts.arn
  protocol  = "email"
  endpoint  = var.email_address

}
