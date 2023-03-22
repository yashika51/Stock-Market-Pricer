import os
from datetime import datetime, timedelta
from typing import Dict

import requests

from currency_data import CurrencyData
from exceptions import MethodException
from utils import (convert_datetime_to_str_date, convert_str_date_to_datetime,
                   increase_date)


class StockData:
    access_key = os.environ.get("MARKETSTACK_API_KEY")
    currency_data = CurrencyData()

    def edge_case_market_closed_on_start_date(
        self, symbol: str, current_date: datetime
    ) -> int:
        """If the market was closed on start date,
        we make request to the day
        before the start date"""
        try:
            previous_datetime = current_date - timedelta(1)
            previous_processed_date = previous_datetime.strftime("%Y-%m-%d")

            request_url = "http://api.marketstack.com/v1/eod/" \
                          f"{previous_processed_date}" \
                          f"&symbol={symbol}"

            params = {"access_key": self.access_key}
            response = requests.get(request_url, params=params).json()

            close_date_amount = response.get("close", 0)
            return close_date_amount

        except Exception as e:
            raise MethodException(f"Exception {e} occurred while running"
                  f" edge_case_market_closed_on_start_date()")

    def get_stock_data_from_api(
        self, symbol: str, start_date: str, end_date: str
    ) -> Dict:
        """Get stock prices from marketstack API"""
        try:
            params = {"access_key": self.access_key}
            request_url_stock_data = f"http://api.marketstack.com/v1/eod?" \
                                     f"access_key={self.access_key}" \
                                     f"&symbols={symbol}"\
                                     f"&date_from={start_date}&" \
                                     f"date_to={end_date}&sort=ASC"

            stock_data_response = requests.get(request_url_stock_data,
                                               params=params)
            stock_data_json = stock_data_response.json()
            stock_data = stock_data_json.get("data", {})

            stock_data_to_return = {}   # type: ignore
            current_expected_date = start_date

            for data in stock_data:
                current_date = convert_datetime_to_str_date(
                    convert_str_date_to_datetime(data.get("date"))
                )

                if current_date != current_expected_date:
                    while current_date != current_expected_date:
                        previous_price = list(stock_data_to_return.values())
                        stock_data_to_return.update({
                            current_expected_date: previous_price[-1]
                            }
                        )
                        current_expected_date = increase_date(
                            current_expected_date, 1)
                        if current_date == current_expected_date:
                            stock_data_to_return.update({
                                current_date: data.get("close")
                            })
                    continue

                else:
                    stock_data_to_return.update({
                        current_date: data.get("close")
                    })
                    current_expected_date = increase_date(
                        current_expected_date, 1)
            return stock_data_to_return

        except Exception as e:
            raise MethodException(f"Exception {e} occurred while running"
                  f" get_close_day_stock_data()")

    def stock_data_with_conversion(
        self,
        start_date: str,
        end_date: str,
        base_currency: str,
        response_currency: str,
        symbol: str,
    ) -> Dict:
        """Convert stock prices to request currency price"""
        try:
            processed_currency_data = self.currency_data.\
                get_currency_data_from_api(
                    start_date, end_date, base_currency,
                    response_currency
                )

            processed_stock_data = self.get_stock_data_from_api(
                symbol, start_date, end_date
            )
            converted_stock_price = {}

            for date, stock_price in processed_stock_data.items():
                currency_conversion = processed_currency_data[date]
                converted_stock_price.update({
                    date: stock_price * currency_conversion
                })

            return converted_stock_price

        except Exception as e:
            raise MethodException(f"Exception {e} occurred while running"
                  f" stock_data_with_conversion()")
