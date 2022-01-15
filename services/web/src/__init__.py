from flask import Flask, render_template, send_from_directory
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_executor import Executor

from . import config


# Initialize app, assets (SASS) and db
app = Flask(__name__)
#Scss(app, static_dir='src/static/styles', asset_dir='src/assets')
app.config.from_object(config.Config)
db = SQLAlchemy(app)


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


# Create an executor instance to run websocket in background.
executor = Executor(app)


# Open alpaca websocket connection using executor.
@app.before_first_request
def start_websocket():
    from .alpaca_api import alpaca_websocket
    executor.submit(alpaca_websocket.open_websocket)


from .routes.quotes import quotes as quotes_blueprint
# blueprint for quotes api routes
app.register_blueprint(quotes_blueprint)

from .routes.auth import auth as auth_blueprint
# blueprint for auth routes
app.register_blueprint(auth_blueprint)

from .routes.main import main as main_blueprint
# blueprint for non-auth parts
app.register_blueprint(main_blueprint)


# Route to serve static files
@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)
