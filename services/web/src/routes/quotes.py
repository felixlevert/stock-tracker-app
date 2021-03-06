from flask import Blueprint, request, jsonify, Response, abort
from marshmallow import Schema, fields
from ..models.Stock import Stock

quotes = Blueprint('quotes', __name__)


@quotes.route('/quotes', methods=['GET'])
def get_quotes():
    class QuerySchema(Schema):
        t = fields.Str(required=True)

    schema = QuerySchema()

    args = request.args
    errors = schema.validate(args)
    if errors:
        abort(400, str(errors))

    ticker_list = args.getlist('t')
    if ticker_list[0] == '':
        abort(400, 'No tickers supplied.')
    data = {}
    try:
        for ticker in ticker_list:
            stock = Stock.query.filter_by(ticker=ticker).first()
            data[ticker] = {'price': stock.price, 'open': stock.price_open}
        response = jsonify(data)
        return response
    except Exception:
        return 404


@quotes.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
