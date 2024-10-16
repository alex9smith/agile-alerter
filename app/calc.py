import datetime
from statistics import mean

from type import PricingResult
from typing import List


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
