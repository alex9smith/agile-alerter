from sys import path
from test.fixtures import pricing_results

path.append("./app")
from app.calc import (
    calc_evening_peak,
    calc_midday_average,
    calc_morning_peak,
    calc_overnight_average,
)


class TestCalc:
    def test_calc_overnight_average(self):
        assert calc_overnight_average(pricing=pricing_results) == 1.0

    def test_calc_morning_peak(self):
        assert calc_morning_peak(pricing=pricing_results) == 5.0

    def test_calc_midday_average(self):
        assert calc_midday_average(pricing=pricing_results) == 10.0

    def test_calc_evening_peak(self):
        assert calc_evening_peak(pricing=pricing_results) == 15.0
