import os
from datetime import datetime, timedelta
from typing import Dict, List

import requests

from currency_data import CurrencyData
from exceptions import MethodException


class StockData:
    access_key = os.environ.get("MARKETSTACK_API_KEY")
    currency_data = CurrencyData()

    def edge_case_market_closed_on_start_date(
        self, symbol: str, date_to_datetime: datetime
    ) -> int:
        """If the market was closed on start date,
        we make one more request to the day
        before the start date"""
        try:
            previous_datetime = date_to_datetime - timedelta(1)
            previous_processed_date = previous_datetime.strftime("%Y-%m-%d")

            request_url = f"http://api.marketstack.com/v1/eod/date" \
                          f"{previous_processed_date}&symbol={symbol}"

            params = {"access_key": self.access_key}
            response = requests.get(request_url, params=params).json()
            close_date_amount = response.get("close", 0)
            return close_date_amount

        except Exception as e:
            # will use logging with a proper setup
            raise MethodException(f"Exception {e} occurred while running"
                  f" edge_case_market_closed_on_start_date()")

    def get_stock_data_from_api(
        self, symbol: str, start_date: str, end_date: str
    ) -> List[dict]:
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

            stock_data_to_return = []  # type: ignore
            for data in stock_data:
                date = data.get("date")
                date_to_datetime = datetime.strptime(date,
                                                     "%Y-%m-%dT%H:%M:%S+%f")

                processed_date = date_to_datetime.strftime("%Y-%m-%d")

                # assuming if the market was closed,
                # it will return None in that case by default we use 0
                amount_close = data.get("close", 0)

                if amount_close == 0:
                    # if the market was closed for some day,
                    # use the previous day data
                    amount_close = (
                        stock_data_to_return[-1].get("close")
                        if len(stock_data_to_return) >= 1
                        else self.edge_case_market_closed_on_start_date(
                            symbol, date_to_datetime
                        )
                    )

                stock_data_to_return_dict = {
                    "date": processed_date,
                    "amount_close": amount_close,
                }

                stock_data_to_return.append(stock_data_to_return_dict)
            return stock_data_to_return

        except Exception as e:
            # will use logging with a proper setup
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

            for data in processed_stock_data:
                date = data.get("date")
                stock_price = data.get("amount_close")
                currency_conversion = processed_currency_data[date]
                converted_stock_price.update({
                    date: stock_price * currency_conversion
                })

            return converted_stock_price

        except Exception as e:
            # will use logging with a proper setup
            raise MethodException(f"Exception {e} occurred while running"
                  f" stock_data_with_conversion()")
