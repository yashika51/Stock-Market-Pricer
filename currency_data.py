import os
from typing import Dict

import requests

from exceptions import MethodException


class CurrencyData:
    api_key = os.environ.get("EXCHANGE_RATE_API")

    def get_currency_data_from_api(
            self, start_date: str, end_date: str,
            base_currency: str, response_currency: str
    ) -> Dict:
        try:
            request_url_currency_data = "https://api.apilayer.com/" \
                                        "exchangerates_data/timeseries?" \
                                        f"start_date={start_date}&" \
                                        f"end_date={end_date}&" \
                                        f"base={base_currency}" \
                                        f"&symbols={response_currency}"
            headers = {"apikey": self.api_key}
            currency_data_response = requests.get(
                request_url_currency_data, headers=headers
            )
            currency_data = currency_data_response.json()
            currency_data_rates = currency_data.get("rates", {})

            currency_data_dict = {}

            for date, value in currency_data_rates.items():
                currency_value = value.get(response_currency, None)
                currency_data_dict.update({date: currency_value})

            return currency_data_dict

        except Exception as e:
            # will use logging with a proper setup
            raise MethodException(f"Exception {e} occurred while running"
                                  f" get_currency_data_from_api()")
