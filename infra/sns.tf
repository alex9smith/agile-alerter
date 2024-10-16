resource "aws_sns_topic" "pricing_alerts" {
  name = "pricing_alerts_topic"
  tags = var.resource_tags
}

resource "aws_sns_topic_subscription" "email_subscription" {
  for_each = toset(var.email_addresses)

  topic_arn = aws_sns_topic.pricing_alerts.arn
  protocol  = "email"
  endpoint  = each.key

}
