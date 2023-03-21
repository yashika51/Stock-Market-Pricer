from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_currency_format_invalid():
    response = client.get(
        "/stock-close-prices",
        json={"stock_symbol": "AAPL",
              "currency": "US",
              "date_range": "2023/01/10-2023/02/15"},
    )
    assert response.status_code == 400
    assert response.json() == {
          "detail": "Invalid Currency Format"
    }


def test_stock_price_get_request():
    response = client.get(
        "/stock-close-prices",
        json={"stock_symbol": "MSFT",
              "currency": "EUR",
              "date_range": "2023/02/01-2023/02/05"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "symbol": "MSFT",
        "currency": "EUR",
        "daily_close": {
            "2023-02-01": 229,
            "2023-02-02": 242,
            "2023-02-03": 238
        }
    }


def test_stock_price_get_date_format_with_month_name():
    response = client.get(
        "/stock-close-prices",
        json={"stock_symbol": "MSFT",
              "currency": "INR",
              "date_range": "February 17, 2023 - March 15 2023"
              },
    )
    assert response.status_code == 200
    assert response.json() == {
        "symbol": "MSFT",
        "currency": "INR",
        "daily_close": {
            "2023-02-17": 21371,
            "2023-02-21": 20936,
            "2023-02-22": 20833,
            "2023-02-23": 21048,
            "2023-02-24": 20668,
            "2023-02-27": 20676,
            "2023-02-28": 20610,
            "2023-03-01": 20297,
            "2023-03-02": 20680,
            "2023-03-03": 20860,
            "2023-03-06": 21025,
            "2023-03-07": 20859,
            "2023-03-08": 20794,
            "2023-03-09": 20694,
            "2023-03-10": 20388,
            "2023-03-13": 20927,
            "2023-03-14": 21464,
            "2023-03-15": 21956
        }
    }


def test_stock_price_get_date_format_with_dot_separator():
    response = client.get(
        "/stock-close-prices",
        json={"stock_symbol": "AAPL",
              "currency": "AUD",
              "date_range": "01.01.2023-02.02.2023"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "symbol": "AAPL",
        "currency": "AUD",
        "daily_close": {
            "2023-01-03": 185,
            "2023-01-04": 185,
            "2023-01-05": 185,
            "2023-01-06": 188,
            "2023-01-09": 188,
            "2023-01-10": 189,
            "2023-01-11": 193,
            "2023-01-12": 191,
            "2023-01-13": 193,
            "2023-01-17": 194,
            "2023-01-18": 194,
            "2023-01-19": 195,
            "2023-01-20": 198,
            "2023-01-23": 200,
            "2023-01-24": 202,
            "2023-01-25": 199,
            "2023-01-26": 202,
            "2023-01-27": 204,
            "2023-01-30": 202,
            "2023-01-31": 204,
            "2023-02-01": 203,
            "2023-02-02": 213
        }
    }
