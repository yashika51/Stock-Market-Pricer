from fastapi import FastAPI

from stock_close_price_api import stock_api_router

app = FastAPI()

app.include_router(stock_api_router)
