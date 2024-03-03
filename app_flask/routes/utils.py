'''
    Util routes like health checks and availability
'''

from flask import Blueprint, jsonify
from config import ACTIVE_API_VERSION

utils_bp = Blueprint("utils", __name__)

def hello():
    '''
        use me to do quick check health
        checks if all connections are available
    '''
    data = {'message': f'{ACTIVE_API_VERSION} API is available'}
    return jsonify(data)
