import os
import websocket
import json
from .. import stock_prices
#from dotenv import load_dotenv

#load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

def on_message(ws, message):
    msg = json.loads(message)
    data = msg['data']
    if data['ev'] == 'T':
        print("HEREEEEEE")
        ticker = data["T"]
        if stock_prices.quotes[ticker]:
            stock_prices.quotes[ticker] = data["p"]
        print(f'*****TICKER*****= {ticker} PRICE = {data["p"]}**********')
    

def on_error(ws, error):
    #print(error)
    pass

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    auth = {
        "action": "authenticate",
        "data": {
            "key_id": os.getenv('ALPACA_API_KEY_ID'),
            "secret_key": os.getenv('ALPACA_SECRET_KEY')
        }
    }
    ws.send(json.dumps(auth))
    
    
    ticker_list = []
    for stock in stock_prices.quotes:
        ticker_list.append(f"T.{stock}")
 
    subscribe_object = {
        "action": "listen",
        "data": {
            "streams": ticker_list
        }
    }

    ws.send(json.dumps(subscribe_object))
    
    print("### websocket open ###")

 
def open_websocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://data.alpaca.markets/stream',
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
    
    ws.on_open = on_open 
    ws.run_forever()