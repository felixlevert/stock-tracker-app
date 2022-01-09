import threading
import asyncio
import time
import os

quotes = {'AAPL': 179.98, 'NFLX': 579.45}

from alpaca_trade_api import StreamConn
from alpaca_trade_api.common import URL


conn: StreamConn = None

def consumer_thread():
    try:
        # make sure we have an event loop, if not create a new one
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    global conn
    conn = StreamConn(
        'PK087RNANW8OQQ3BR87C',
        'q3t573Ntxx9aChiiKj7eviNyV7WKfakbWyODA4z3',
        base_url=URL('https://paper-api.alpaca.markets'),
        data_url=URL('https://data.alpaca.markets'),
        data_stream='alpacadatav1'
    )


    @conn.on(r'Q\..+')
    async def on_quotes(conn, channel, quote):
        print('quote', quote)


    @conn.on(r'T\..+')
    async def on_trades(conn, channel, trade):
        print('trade', trade)


    conn.run()

if __name__ == '__main__':
    threading.Thread(target=consumer_thread).start()

    loop = asyncio.get_event_loop()

    time.sleep(5)  # give the initial connection time to be established
    

    while 1:
        ticker_list = []
        for stock in quotes:
            ticker_list.append([f'alpacadatav1/T.{stock}'])
        for stock in ticker_list:
            print(f'********{stock}*********')
            loop.run_until_complete(conn.subscribe(stock))
            time.sleep(20)