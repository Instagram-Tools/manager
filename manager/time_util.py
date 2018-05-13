"""Helper module to handle time related stuff"""
import datetime
from random import gauss
from time import sleep as original_sleep

# Amount of variance to be introduced
# i.e. random time will be in the range: TIME +/- STDEV %
STDEV = 0.5
sleep_percentage = 1


def randomize_time(mean):
    allowed_range = mean * STDEV
    stdev = allowed_range / 3  # 99.73% chance to be in the allowed range

    t = 0
    while abs(mean - t) > allowed_range:
        t = gauss(mean, stdev)

    return t


def set_sleep_percentage(percentage):
    global sleep_percentage
    sleep_percentage = percentage / 100


def sleep(t, custom_percentage=None):
    try:
        if custom_percentage is None:
            custom_percentage = sleep_percentage
        time = randomize_time(t) * custom_percentage
        print("sleep: " + str(time))
        original_sleep(time)
        return True

    except Exception as exc:
        print(exc)
        return False


def sleep_actual(t):
    original_sleep(t)


def parse_datetime(line):
    return time_in_week(parse_datetime_prefix(str(line), '%Y-%m-%d %H:%M:%S'))


def time_in_week(dt):
    return datetime.datetime(1, 1, day=dt.isoweekday(), hour=dt.hour, minute=dt.minute, second=dt.second)


def parse_datetime_prefix(line, fmt):
    try:
        t = datetime.datetime.strptime(line, fmt)
    except ValueError as v:
        if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
            line = line[:-(len(v.args[0]) - 26)]
            t = datetime.datetime.strptime(line, fmt)
        else:
            raise
    return t