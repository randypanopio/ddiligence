"""
    routes that use the firestore db
"""
import random
from datetime import datetime
from typing import List, Tuple
from flask import jsonify, Blueprint, request, abort
from firestore.database import db_manager
from routes.utils import validate_and_convert_args
from config import ACTIVE_API_VERSION, DAY_FORMAT

firestore_data_bp = Blueprint("database", __name__)


@firestore_data_bp.route(f'{ACTIVE_API_VERSION}stocks_data', methods=['GET'])
def get_historic_data() -> str:
    """_summary_

    :return: _description_
    :rtype: str
    """
    # Check required arguements
    arg_ticker = request.args.get('ticker')
    arg_date_start = request.args.get('date_start')
    arg_date_end = request.args.get('date_end')

    # Validate and convert ticker argument
    v_ticker, ticker = validate_and_convert_args('ticker', arg_ticker, str)
    if not v_ticker:
        print(ticker)
        abort(400, description={'error': ticker})

    # Validate and convert date_start argument
    v_date_start, date_start = validate_and_convert_args(
        'date_start',
        arg_date_start,
        datetime,
        datetime.strptime,
        *(arg_date_start, DAY_FORMAT))
    if not v_date_start:
        print(date_start)
        abort(400, description={'error': date_start})

    # Validate and convert date_end argument
    v_date_end, date_end = validate_and_convert_args(
        'date_end',
        arg_date_end,
        datetime,
        datetime.strptime,
        *(arg_date_end, DAY_FORMAT))
    if not v_date_end:
        abort(400, description={'error': date_end})

    # check if ticker avail
    if ticker not in db_manager.get_available_tickers():
        abort(404, description={'error': f"ticker {ticker} not found"})

    # check if date range is valid
    try:
        r_start = request.args.get('date_start')
        r_end = request.args.get('date_end')
        start = datetime.strptime(r_start, DAY_FORMAT)
        end = datetime.strptime(r_end, DAY_FORMAT)
    except ValueError:
        message = "something"
        print(message)
        abort(404, description={'error': message})

    # TODO use me to check health, EG if other external api i would be usingis available, if db is avail, etc.
    data = {'message': f'{ACTIVE_API_VERSION} API is available'}
    return jsonify(data)


@firestore_data_bp.route(f'{ACTIVE_API_VERSION}banner_messages', methods=['GET'])
def get_daily_banner_messages() -> List[Tuple[str, str, List[str]]]:
    '''
        Retrieves randomized set of available banner messages    
    '''
    messages = db_manager.get_daily_messages()

    # TODO create season and themes for the messages, (Use tags to influence seed)
    # Generate today's seed based on the current date
    # TODO it should be by location and timezone too
    seed = datetime.utcnow().strftime('%Y-%m-%d')
    random.seed(seed)

    # select up to 10 random indices from seed
    num_messages = len(messages)
    random_indices = random.sample(range(num_messages), min(10, num_messages))

    # list comp filtered messages with random indices
    filtered_messages = [messages[i] for i in random_indices]
    return jsonify(filtered_messages)
