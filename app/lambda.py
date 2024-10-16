import datetime
from os import getenv
import boto3
import requests
from constants import PRICING_BASE_URL
from aws_lambda_powertools.logging import Logger
from calc import (
    calc_evening_peak,
    calc_midday_average,
    calc_morning_peak,
    calc_overnight_average,
)
from dates import get_tomorrow_period, london_tz

from type import Period, PricingResponse
from aws_lambda_powertools.utilities.typing import LambdaContext

REGIONAL_PRICING_BASE_URL = PRICING_BASE_URL.replace("REGION", getenv("REGION"))
logger = Logger(service="agile-alerter")


def get_pricing() -> PricingResponse:
    response = requests.get(REGIONAL_PRICING_BASE_URL, params=get_tomorrow_period())
    pricing: PricingResponse = response.json()

    # Parse all the dates upfront
    # The API returns datetimes in UTC so convert back to London time
    for result in pricing["results"]:
        result["valid_from"] = datetime.datetime.fromisoformat(
            result["valid_from"]
        ).astimezone(london_tz)
        result["valid_to"] = datetime.datetime.fromisoformat(
            result["valid_to"]
        ).astimezone(london_tz)

    return pricing


def build_message(pricing: PricingResponse) -> str:
    return f"""
    Overnight: {calc_overnight_average(pricing["results"]):.1f}p
    Morning peak: {calc_morning_peak(pricing["results"]):.1f}p
    Midday average: {calc_midday_average(pricing["results"]):.1f}p
    Evening peak: {calc_evening_peak(pricing["results"]):.1f}p

    View pricing breakdown: https://octopus.energy/dashboard/new/accounts
    """


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> None:
    logger.info("Getting pricing")
    pricing = get_pricing()
    logger.info("Building message")
    message = build_message(pricing)

    logger.info("Setting up SNS client")
    client = boto3.client("sns")
    logger.info("Publishing to SNS")
    client.publish(
        TopicArn=getenv("TOPIC_ARN"),
        Message=message,
        Subject="Octopus Agile prices for tomorrow",
    )
    logger.info("Finished")
