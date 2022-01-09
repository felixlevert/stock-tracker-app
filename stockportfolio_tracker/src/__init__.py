import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from . import config
from flask_executor import executor




db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    env_config = os.getenv('APP_SETTINGS')
    app.config.from_object(config.DevelopmentConfig)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
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
        # get quotes from my API
        pass


    # blueprint for auth routes in app
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app