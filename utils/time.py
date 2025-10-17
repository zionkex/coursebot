from datetime import datetime, time, timedelta
from enum import Enum


class TimeEnum(Enum):
    two_hour = "2 години"
    fifteen_minutes = "15 хвилин"


def add_hours_to_time(t: time, hours: int = 1) -> time:
    dt = datetime.combine(datetime.today(), t)
    return (dt + timedelta(hours=hours)).time()


def get_hour_for_reminder(start_time: time, delta, hours: bool = True):
    dt = datetime.combine(datetime.today(), start_time)
    if hours < 10:
        return (dt - timedelta(minutes=delta)).time()
    else:
        return (dt - timedelta(minutes=delta)).time()


def change_time_to_user_zone(utc_time: time, delta: int):
    dt = datetime.combine(datetime.today(), utc_time)
    return dt - timedelta(hours=delta)
