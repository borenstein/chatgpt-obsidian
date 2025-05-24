from datetime import datetime, timezone


def epoch_to_dt(epoch_time: float) -> datetime:
    return datetime.fromtimestamp(epoch_time, tz=timezone.utc)

def epoch_to_date(epoch_time: float) -> str:
    dt: datetime = epoch_to_dt(epoch_time)
    return dt.strftime("%Y-%m-%d")

def epoch_to_human_timestamp(epoch_time: float) -> str:
    dt = epoch_to_dt(epoch_time)
    return dt.strftime("%A, %B {day}, %Y %H:%M:%S UTC").format(day=dt.day)
