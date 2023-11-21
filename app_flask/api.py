from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import stock_data as sd


app = Flask(__name__)
CORS(app)

v_prefix = '/api/v1/'

@app.route(f'{v_prefix}hello')
def hello():
    # TODO use me to check health, EG if other external api i would be usingis available, if db is avail, etc.
    data = {'message': f'{v_prefix} API is available'}
    return jsonify(data)

#TODO caching when data retrieval when no new data is avail

@app.route(f'{v_prefix}stock_history')
def get_historic_data():
    ticker = request.args.get('ticker')
    if sd.is_available(ticker):
        return jsonify(sd.get_data(ticker))
    else:
        message = {'error': f'Stock {ticker} was not found or is not available'}
        abort(404, description=message)


if __name__ == '__main__':
    app.run(debug=True)