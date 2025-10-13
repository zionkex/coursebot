from datetime import datetime, time, timedelta


def add_hours_to_time(t: time, hours: int = 1) -> time:
    dt = datetime.combine(datetime.today(), t)
    return (dt + timedelta(hours=hours)).time()
