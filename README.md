# Stock Close Day Prices

This repo contains code for getting stocks close day prices based on the input currency.

## Setup

Create a new virtual environment either using conda or pythong venv, and install all the requirements
from `requirements.txt` file. After that setup your credentials, create an `.env` file and add `MARKETSTACK_API_KEY` and `EXCHANGE_RATE_API`
with the values.


## Consuming the API

You can test the API by Postman, run `uvicorn main:app --reload` command in the terminal
and go to Postman, make a GET request to endpoint `http://127.0.0.1:8000/stock-close-prices`
and pass the request data in JSON format.

Example Input:

```{
    "stock_symbol": "AAPL",
    "currency": "EUR",
    "date_range": "2023/02/20-2023/03/21"
    }
```


## Running Tests

After the setup, you can run `pytest tests.py` in your terminal to run 4 test cases. After successful setup
you should be able to see passed test cases.



A quick overview of the files present in the repo:

- `.gitignore`: To ignore cache and environment files
- `currency_data.py`: Contains the logic to get the currency data from the API
- `exceptions.py`: Contains custom exception
- `format.sh`: Shell script with steps to format and run lint on all the files present
- `main.py`: For adding the API route
- `requirements.txt`: Requirements with versions used for the task
- `schemas.py`: Schema for request and response
- `stock_close_price_api.py`: API file with the endpoint calling utils and other methods
- `stock_data.py`: Logic for getting the stock data as well converting stock prices based on currency conversions
- `tests.py`: Contains test cases
- `utils.py`: Contains helper functions consumed by other functions


## Assumptions

Some assumptions made are:

- The market is open on start and end dates, hence passing the date range. Method `edge_case_market_closed_on_start_date` in `stock_data.py` is something we can expand
on but the initial idea is to use the `http://api.marketstack.com/v1/eod/{previous_processed_date}` endpoint to get the data of a particular day outside the date range.

- APIs return the data without limitation. Adding `limits` and `offsets` to the request calls is something that can be additionally done.

## Date Formats

Currently we are handling multiple cases for dates possible for example
    o Month-Day-Year with leading zeros (02/17/2009)
    o Day-Month-Year with leading zeros and dots as separators (17.02.2009)
    o Month name Day, Year like this (February 17, 2009)

But the input is in string format separated by "-" for example `10.01.2022-10.02.2022`. A better approach could be to use
datetime instead and separate inputs for start date and end date, this will also help to eliminate helper functions that are currently
being used for processing dates from datetime to string and vice versa. We can modify `StockPriceRequest` in `schemas.py` to have
two new fields `start_date` and `end_date` with type `datetime` and eliminate `date_range`. Also a better approach could be to make
it non optional and having the user add dates in request before calling the endpoint.



