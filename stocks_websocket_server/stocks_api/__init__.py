import os
from flask import Flask, render_template
from flask_executor import Executor
import psycopg2
import threading
import signal
import sys
from .websocket_listen import alpaca_websocket
from . import stock_prices
from . import config


def create_app():
    app = Flask(__name__)
    env_config = os.getenv('APP_SETTINGS')
    app.config.from_object(config.DevelopmentConfig)

    @app.before_first_request
    def get_prices():
        conn = None;
        try:
            conn = psycopg2.connect(database='portfolio_tracker_db_dev')
            cur = conn.cursor()
            cur.execute("SELECT ticker, price FROM stocks")
            rows = cur.fetchall()
            for row in rows:
                stock_prices.quotes[row[0]] = row[1]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
    executor = Executor(app)

    @app.before_first_request
    def start_websocket():
        executor.submit(alpaca_websocket.open_websocket)

    from .routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app