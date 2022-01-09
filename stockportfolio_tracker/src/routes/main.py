from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .. import db
from ..models.Portfolio import Portfolio
from ..models.Stock import Stock

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    portfolio = Portfolio.portfolio_builder(user_id=current_user.id)
    return render_template('index.html', name=current_user.name, portfolio=portfolio)

# @main.context_processor
# def inject_prices():
#     portfolio = Portfolio.portfolio_builder(user_id=current_user.id)
#     stock_prices = {}
#     for p in portfolio:
#         stock_prices[p['ticker']] = p['price']
#     return stock_prices

@main.route('/add-stock', methods=['POST'])
def add_stock():
    user_id = current_user.id
    ticker = request.form.get('ticker')
    quantity = request.form.get('quantity')
    price = request.form.get('price')

    # Check if stock already in db, add to stocks db if not
    stock = Stock.query.filter_by(ticker=ticker).first()
    if not stock:
        price = price # ********CHANGE THIS SO IT GETS THE PRICE FROM THE API!!!*******
        stock = Stock(ticker=ticker, name="name", price=price)
        db.session.add(stock)
        db.session.commit()
    
    stock_id = Stock.query.filter_by(ticker=ticker).first().id
    
    # Check if user already holds this asset
    portfolio_entry = Portfolio.query.filter_by(stock_id=stock_id, user_id=user_id).first()

    if portfolio_entry:
        new_price = float(price)
        new_quantity = float(quantity)
        old_price = float(portfolio_entry.purchase_price)
        old_qty = float(portfolio_entry.quantity)
        new_avg_price = ((new_price * new_quantity) + (old_price * old_qty)) / (old_qty + new_quantity)
        new_avg_price = round(new_avg_price, 2)
        portfolio_entry.purchase_price = new_avg_price
        portfolio_entry.quantity += int(quantity)
        db.session.commit()
    
    else:
        portfolio_entry = Portfolio(user_id=user_id, stock_id=stock_id, quantity=quantity, purchase_price=price)
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
            db.session.commit()

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
    

    
