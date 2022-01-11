from .. import db

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)  
    ticker = db.Column(db.String(100))
    name = db.Column(db.String(1000))    
    price = db.Column(db.Float)

    def __init__(self, ticker, name, price):
        self.ticker = ticker
        self.name = name
        self.price = price

