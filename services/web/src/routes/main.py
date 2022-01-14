from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .. import db
from ..models.Portfolio import Portfolio
from ..models.Stock import Stock
from ..alpaca_api import alpaca_api_calls, alpaca_websocket

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    portfolio = Portfolio.portfolio_builder(user_id=current_user.id)
    return render_template('index.html', name=current_user.name, portfolio=portfolio)


@main.route('/add-stock', methods=['POST'])
def add_stock():
    user_id = current_user.id
    ticker_name = request.form.get('ticker').split('-')
    ticker = ticker_name[0]
    name = ticker_name[1]
    quantity = request.form.get('quantity')
    purchase_price = request.form.get('price')
    open_price = alpaca_api_calls.get_open_price(ticker)

    # Check if stock already in db, add to stocks db if not
    stock = Stock.query.filter_by(ticker=ticker).first()

    # Iinitalize stock_id
    stock_id = None

    if not stock:
        price = alpaca_api_calls.get_quote(ticker)
        stock = Stock(ticker=ticker, name=name, price=price, price_open=open_price)
        db.session.add(stock)
        db.session.commit()
        stock_id = Stock.query.filter_by(ticker=ticker).first().id
        alpaca_websocket.on_subscribe()
    else:
        stock_id = stock.id

    # Check if user already holds this asset
    portfolio_entry = Portfolio.query.filter_by(stock_id=stock_id, user_id=user_id).first()

    # Update entry if exists
    if portfolio_entry:
        new_price = float(purchase_price)
        new_quantity = float(quantity)
        old_price = float(portfolio_entry.purchase_price)
        old_qty = float(portfolio_entry.quantity)
        new_avg_price = ((new_price * new_quantity) + (old_price * old_qty)) / (old_qty + new_quantity)
        new_avg_price = round(new_avg_price, 2)
        portfolio_entry.purchase_price = new_avg_price
        portfolio_entry.quantity += int(quantity)
        db.session.commit()

    # Create new entry if not exists
    else:
        portfolio_entry = Portfolio(user_id=user_id, stock_id=stock_id, quantity=quantity, purchase_price=purchase_price)
        db.session.add(portfolio_entry)
        db.session.commit()

    return redirect('/')


@main.route('/sell-stock', methods=['POST'])
def sell_stock():
    user_id = current_user.id
    ticker = request.form.get('ticker')
    quantity = request.form.get('quantity')
    price = request.form.get('price')

    # find relevant portfolio entry
    stock_id = Stock.query.filter_by(ticker=ticker).first().id
    portfolio_entry = Portfolio.query.filter_by(stock_id=stock_id, user_id=user_id).first()

    if portfolio_entry:
        new_quantity = portfolio_entry.quantity - int(quantity)
        if new_quantity < 1:
            db.session.delete(portfolio_entry)
            # Check if anyone else holds that stock, if not, remove from stocks db
            stock = Stock.query.filter_by(ticker=ticker).first()
            stock_in_portfolio = Portfolio.query.filter_by(stock_id=stock_id).first()
            if not stock_in_portfolio:
                db.session.delete(stock)

        else:
            new_price = float(price)
            new_quantity = float(quantity)
            old_price = float(portfolio_entry.purchase_price)
            old_qty = float(portfolio_entry.quantity)
            new_avg_price = ((old_price * old_qty) - (new_price * new_quantity)) / (old_qty - new_quantity)
            new_avg_price = round(new_avg_price, 2)
            portfolio_entry.purchase_price = new_avg_price
            portfolio_entry.quantity = new_quantity

        db.session.commit()

    return redirect('/')
