import os
import alpaca_trade_api as tradeapi

# Create API object
api = tradeapi.REST(os.getenv('ALPACA_API_KEY_ID'), os.getenv('ALPACA_SECRET_KEY'))


def get_open_price(ticker):

    # Get day bar for ticker
    barset = api.get_barset(ticker, 'day', limit=1)

    # Get open price of bar
    open_price = barset[ticker][0].o
    return open_price


def get_quote(ticker):
    # Get quote for ticker
    quote = api.get_last_trade(ticker).price
    return quote
