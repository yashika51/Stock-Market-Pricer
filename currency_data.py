import os
from typing import Dict

import requests


class CurrencyData:
    api_key = os.environ.get("EXCHANGE_RATE_API")

    def get_currency_data_from_api(
        self, start_date: str, end_date: str, base_currency: str, response_currency: str
    ) -> Dict:
        request_url_currency_data = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={start_date}&end_date={end_date}&base={base_currency}&symbols={response_currency}"
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
