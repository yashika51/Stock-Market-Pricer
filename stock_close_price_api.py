from typing import Optional

from fastapi import APIRouter, HTTPException
from starlette import status

from schemas import StockPriceRequest, StockPriceResponse
from stock_data import StockData
from utils import (convert_date_format, convert_string_uppercase,
                   is_currency_str_valid, last_month_range)

stock_api_router = APIRouter()


@stock_api_router.get("/stock-close-prices")
def get_converted_stock_data(
    request: StockPriceRequest,
) -> Optional[StockPriceResponse]:
    symbol = convert_string_uppercase(request.stock_symbol)
    currency = convert_string_uppercase(request.currency)
    date_range = request.date_range

    start_date, end_date = convert_date_format(date_range) \
        if date_range else last_month_range()

    if is_currency_str_valid(currency):

        stock_data_object = StockData()
        converted_stock_price = stock_data_object.stock_data_with_conversion(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            base_currency="USD",
            response_currency=currency,
        )

        return StockPriceResponse(
            symbol=symbol, currency=currency,
            daily_close=converted_stock_price
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Currency Format",
        )
