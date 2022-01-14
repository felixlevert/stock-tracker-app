from .. import db
from .Stock import Stock


class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stocks.id"), nullable=False)
    quantity = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)

    def __init__(self, user_id, stock_id, quantity, purchase_price):
        self.user_id = user_id
        self.stock_id = stock_id
        self.quantity = quantity
        self.purchase_price = purchase_price

    def portfolio_builder(user_id):
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()

        holdings = []
        for p in portfolio:
            stock = Stock.query.filter_by(id=p.stock_id).first()
            holding = {
                "ticker": stock.ticker,
                "name": stock.name,
                "quantity": p.quantity,
                "purchase_price": p.purchase_price,
                "price": stock.price
            }
            holdings.append(holding)

        return holdings
