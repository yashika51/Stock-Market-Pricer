from typing import Dict, Optional

from pydantic import BaseModel


class StockPriceRequest(BaseModel):
    stock_symbol: str
    currency: str
    date_range:  Optional[str]


class StockPriceResponse(BaseModel):
    symbol: str
    currency: str
    daily_close: Dict[str, int]
