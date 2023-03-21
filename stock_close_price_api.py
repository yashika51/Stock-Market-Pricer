from typing import Optional

from fastapi import APIRouter, HTTPException
from starlette import status

from schemas import StockPriceRequest, StockPriceResponse
from stock_data import StockData
from utils import (convert_date_format, convert_string_uppercase,
                   is_currency_str_valid)

stock_api_router = APIRouter()


@stock_api_router.get("/stock-close-prices")
def get_converted_stock_data(
    request: StockPriceRequest,
) -> Optional[StockPriceResponse]:
    symbol = convert_string_uppercase(request.stock_symbol)
    currency = convert_string_uppercase(request.currency)
    start_date, end_date = convert_date_format(request.date_range)

    if not is_currency_str_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Currency Format",
        )

    stock_data_object = StockData()
    converted_stock_price = stock_data_object.stock_data_with_conversion(
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        base_currency="USD",
        response_currency=currency,
    )

    return StockPriceResponse(
        stock_symbol=symbol, currency=currency,
        closing_price=converted_stock_price
    )
