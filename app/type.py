from datetime import datetime
from typing import TypedDict, List


class Period(TypedDict):
    period_from: str
    period_to: str


class RegionPricing(TypedDict):
    multiplier: float
    peak_adder: int


class PricingResult(TypedDict):
    value_exc_vat: float
    value_inc_vat: float
    valid_from: datetime
    valid_to: datetime
    payment_method: None


class PricingResponse(TypedDict):
    count: int
    previous: str | None
    next: str | None
    results: List[PricingResult]
