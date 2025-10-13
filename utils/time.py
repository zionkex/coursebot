from datetime import datetime, time, timedelta


def add_hours_to_time(t: time, hours: int = 1) -> time:
    dt = datetime.combine(datetime.today(), t)
    return (dt + timedelta(hours=hours)).time()


def get_hour(start_time: time, delta, hours: bool = True):
    dt = datetime.combine(datetime.today(), start_time)
    if hours < 10:
        return (dt - timedelta(hours=delta)).time()
    else:
        return (dt - timedelta(minutes=delta)).time()
