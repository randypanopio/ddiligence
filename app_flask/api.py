from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/hello')
def hello():
    data = {'message': 'Hello'}
    return jsonify(data)


@app.route('/api/ticker_data', methods=['GET'])
def get_historic_data(ticker):
    data = {}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)