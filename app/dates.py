from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from type import Period

utc_tz = ZoneInfo("Etc/UTC")
london_tz = ZoneInfo("Europe/London")


# Get tomorrow in London time converted to UTC for the API call
def get_tomorrow_period() -> Period:
    now = datetime.now()
    tomorrow_start = datetime(
        now.year, now.month, now.day, tzinfo=london_tz
    ) + timedelta(days=1)
    tomorrow_end = datetime(
        now.year, now.month, now.day, 23, 59, tzinfo=london_tz
    ) + timedelta(days=1)

    return {
        "period_from": f"{tomorrow_start.astimezone(utc_tz).strftime("%Y-%m-%dT%H:%MZ")}",
        "period_to": f"{tomorrow_end.astimezone(utc_tz).strftime("%Y-%m-%dT%H:%MZ")}",
    }
