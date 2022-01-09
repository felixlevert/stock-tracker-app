from flask import Blueprint, request, jsonify, Response
from marshmallow import Schema, fields
from ..stock_prices import quotes

api = Blueprint('api', __name__)

@api.route('/quotes', methods=['GET'])
def get_quotes():
    class QuerySchema(Schema):
        t = fields.Str(required=True)

    schema = QuerySchema()


    args = request.args
    errors = schema.validate(request.args)
    if errors:
        abort(400, str(errors))

    ticker_list = request.args.getlist('t')
    data = {}
    for ticker in ticker_list:
        data[ticker] = quotes[ticker]
    response = jsonify(data)
    return response

@api.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# @api.route('/add', methods=['GET', 'POST'])
# def post_add_stock():
#     class QuerySchema(Schema):
#         t = fields.Str(required=True)

#     schema = QuerySchema()

#     def signal_handler(signal, frame):
#         print("exiting")
#         sys.exit(0)

#     args = request.args
#     errors = schema.validate(request.args)
#     if errors:
#         abort(400, str(errors))

#     ticker_info = request.args.getlist('t')
#     ticker = ticker_info[0]
#     price = ticker_info[1]
#     quotes.append({ticker: float(price)})
#     return 'success', 204