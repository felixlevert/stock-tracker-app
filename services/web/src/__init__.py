import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_executor import Executor
import psycopg2
from . import config


#def create_app():
app = Flask(__name__)

#env_config = os.getenv('APP_SETTINGS')
app.config.from_object(config.Config)


db = SQLAlchemy(app)

#db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models.User import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Populate stock prices on server startup
@app.before_first_request
def populate_prices():
    from .models.Stock import Stock
    from .alpaca_api import alpaca_api_calls
    stock_list = Stock.query.all()
    for stock in stock_list:
        stock.price = alpaca_api_calls.get_quote(stock.ticker)
        db.session.commit()

executor = Executor(app)

@app.before_first_request
def start_websocket():
    from .alpaca_api import alpaca_websocket
    executor.submit(alpaca_websocket.open_websocket)

from .routes.quotes import quotes as quotes_blueprint
app.register_blueprint(quotes_blueprint)


# blueprint for auth routes in app
from .routes.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .routes.main import main as main_blueprint
app.register_blueprint(main_blueprint)


    #return app