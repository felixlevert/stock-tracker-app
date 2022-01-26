import os
import time
import alpaca_trade_api as tradeapi
from ..models.Stock import Stock
from .. import db

# Create API object
api = tradeapi.REST(os.getenv('ALPACA_API_KEY_ID'), os.getenv('ALPACA_SECRET_KEY'))


def get_open_price(ticker):

    # Get day bar for ticker
    barset = api.get_barset(ticker, 'day', limit=1)

    # Get open price of bar
    open_price = barset[ticker][0].o
    return open_price


def open_prices_process():
    while (True):
        stock_list = Stock.query.all()

        for stock in stock_list:
            try:
                # Get day bar for ticker
                barset = api.get_barset(stock.ticker, 'day', limit=1)

                # Get open price of bar
                open_price = barset[stock.ticker][0].o
                stock.open_price = open_price
                db.session.commit()
                print(f"UPDATED OPEN PRICE: {stock.ticker}: {open_price}")
            except Exception:
                print(f"Error getting open price for {stock.ticker}")

        time.sleep(1000)


def get_quote(ticker):
    # Get quote for ticker
    quote = api.get_last_trade(ticker).price
    return quote
