import os
import websocket
import json
from ..models.Stock import Stock
from .. import db


basedir = os.path.abspath(os.path.dirname(__file__))


def on_message(ws, message):
    msg = json.loads(message)
    data = msg['data']
    try:
        if data['ev'] == 'T':
            ticker = data['T']
            stock = Stock.query.filter_by(ticker=ticker).first()
            stock.price = data['p']
            db.session.commit()
    except Exception:
        print("Didn't write to db")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


ws = websocket.WebSocketApp('wss://data.alpaca.markets/stream',
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)


def on_subscribe():
    stock_list = Stock.query.all()
    ticker_list = []
    for stock in stock_list:
        ticker_list.append(f"T.{stock.ticker}")

    subscribe_object = {
        "action": "listen",
        "data": {
            "streams": ticker_list
        }
    }
    # Send subscribe object to websocket.
    ws.send(json.dumps(subscribe_object))


def on_open(ws):
    auth = {
        "action": "authenticate",
        "data": {
            "key_id": os.getenv('ALPACA_API_KEY_ID'),
            "secret_key": os.getenv('ALPACA_SECRET_KEY')
        }
    }
    # Send auth object to websocket.
    ws.send(json.dumps(auth))
    # Subscribe to websocket.
    on_subscribe()
    print("### websocket open ###")


def open_websocket():
    websocket.enableTrace(True)
    ws.on_open = on_open
    ws.run_forever()
