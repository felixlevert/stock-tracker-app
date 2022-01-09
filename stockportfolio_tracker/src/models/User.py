from flask_login import UserMixin
from .. import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
