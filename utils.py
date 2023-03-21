from datetime import datetime, timedelta
from typing import Tuple

from dateutil import parser


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
    start_date_datetime = end_date_datetime-timedelta(30)

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
