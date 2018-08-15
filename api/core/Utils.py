from datetime import datetime


def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
