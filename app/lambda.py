import datetime
from os import getenv
from statistics import mean
import boto3
import requests
from constants import PRICING_BASE_URL
from aws_lambda_powertools.logging import Logger

from typing import List
from type import Period, PricingResponse, PricingResult
from aws_lambda_powertools.utilities.typing import LambdaContext

REGIONAL_PRICING_BASE_URL = PRICING_BASE_URL.replace("REGION", getenv("REGION"))
logger = Logger(service="agile-alerter")


def get_tomorrow_period() -> Period:
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return {
        "period_from": f"{tomorrow.strftime("%Y-%m-%d")}T00:00Z",
        "period_to": f"{tomorrow.strftime("%Y-%m-%d")}T23:59Z",
    }


def get_pricing() -> PricingResponse:
    response = requests.get(REGIONAL_PRICING_BASE_URL, params=get_tomorrow_period())
    pricing: PricingResponse = response.json()

    # parse all the dates upfront
    for result in pricing["results"]:
        result["valid_from"] = datetime.datetime.fromisoformat(result["valid_from"])
        result["valid_to"] = datetime.datetime.fromisoformat(result["valid_to"])

    return pricing


def calc_overnight_average(pricing: List[PricingResult]) -> float:
    # Overnight is earlier than 4AM
    return mean(
        r["value_inc_vat"]
        for r in pricing
        if r["valid_from"].time() < datetime.time(4, 0)
    )


def calc_morning_peak(pricing: List[PricingResult]) -> float:
    # Between 7AM and 9AM
    return mean(
        r["value_inc_vat"]
        for r in pricing
        if (
            (r["valid_from"].time() >= datetime.time(7, 0))
            and (r["valid_from"].time() < datetime.time(9, 0))
        )
    )


def calc_midday_average(pricing: List[PricingResult]) -> float:
    # Between 10AM and 4PM
    return mean(
        r["value_inc_vat"]
        for r in pricing
        if (
            (r["valid_from"].time() >= datetime.time(10, 0))
            and (r["valid_from"].time() < datetime.time(16, 0))
        )
    )


def calc_evening_peak(pricing: List[PricingResult]) -> float:
    # Between 4PM and 7PM
    return mean(
        r["value_inc_vat"]
        for r in pricing
        if (
            (r["valid_from"].time() >= datetime.time(16, 0))
            and (r["valid_from"].time() < datetime.time(19, 0))
        )
    )


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
