from datetime import datetime, timedelta
from typing import Optional, Tuple

from dateutil import parser


def convert_date_format(date_range: Optional[str]) -> Tuple:
    if date_range:
        dates = date_range.split("-")
        start_date, end_date = dates
        start_date_datetime = parser.parse(start_date)
        end_date_datetime = parser.parse(end_date)
    else:
        # if the data_field is empty, return data for last one month
        start_date_datetime = datetime.now()
        end_date_datetime = datetime.now()-timedelta(30)

    start_date = start_date_datetime.strftime('%Y-%m-%d')
    end_date = end_date_datetime.strftime('%Y-%m-%d')

    return start_date, end_date


def convert_string_uppercase(input_string: str) -> str:
    return input_string.upper()


def is_currency_str_valid(currency: str) -> bool:
    """Check currency is exactly 3 character long and isalpha"""

    if len(currency) != 3 and currency.isalpha():
        return False

    else:
        return True
