from typing import Dict, Optional

from pydantic import BaseModel


class StockPriceRequest(BaseModel):
    stock_symbol: str
    currency: str
    date_range:  Optional[str]


class StockPriceResponse(BaseModel):
    stock_symbol: str
    currency: str
    closing_price: Dict[str, int]
