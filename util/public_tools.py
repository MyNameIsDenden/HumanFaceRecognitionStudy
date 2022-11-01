import random
import datetime
from entity import organizations as o


def randomNumber(len):
    first = str(random.randint(1, 9))
    last = "".join(random.sample("1234567890", len - 1))
    return first + last


def randomCode():
    return randomNumber(o.CODE_LEN)


def valid_time(str):
    try:
        datetime.datetime.strptime(str, "%H:%M:%S")
        return True
    except:
        return False


def valid_year_month(str):
    try:
        datetime.datetime.strptime(str, "%Y-%m")
        return True
    except:
        return False


def valid_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False
