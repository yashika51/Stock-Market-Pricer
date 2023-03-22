from datetime import datetime, timedelta
from typing import Tuple

from dateutil import parser


def convert_str_date_to_datetime(date: str) -> datetime:
    """Convert string date to datetime"""
    date_datetime = datetime.strptime(date,
                                      "%Y-%m-%dT%H:%M:%S+%f")
    return date_datetime


def increase_date(date: str, days: float) -> str:
    """Increase input date string date by input number of days"""
    date_datetime = datetime.strptime(date,
                                      "%Y-%m-%d")
    return convert_datetime_to_str_date(date_datetime + timedelta(days=days))


def convert_datetime_to_str_date(date: datetime) -> str:
    """Convert datetime date to str date"""
    date_str = date.strftime("%Y-%m-%d")
    return date_str


def convert_date_format(date_range: str) -> Tuple:
    """Convert request date format to API acceptable format"""

    dates = date_range.split("-")
    start_date, end_date = dates
    start_date_datetime = parser.parse(start_date)
    end_date_datetime = parser.parse(end_date)
    start_date = start_date_datetime.strftime('%Y-%m-%d')
    end_date = end_date_datetime.strftime('%Y-%m-%d')

    return start_date, end_date


def last_month_range() -> Tuple:
    """If the data_field is empty, return date range for last one month"""
    end_date_datetime = datetime.now()
    start_date_datetime = end_date_datetime - timedelta(30)

    start_date = start_date_datetime.strftime('%Y-%m-%d')
    end_date = end_date_datetime.strftime('%Y-%m-%d')

    return start_date, end_date


def convert_string_uppercase(input_string: str) -> str:
    """Convert input string to uppercase"""
    return input_string.upper()


def is_currency_str_valid(currency: str) -> bool:
    """Check currency is exactly 3 character long and isalpha"""

    if len(currency) == 3 and currency.isalpha():
        return True

    return False
