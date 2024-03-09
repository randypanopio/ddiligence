"""
    routes that use the firestore db
"""
import hashlib
import random
from datetime import datetime
from flask import jsonify, Blueprint, request, abort

from firestore.database import db_manager
from routes.utils import validate_and_convert_args, validate_date_range
from config import ACTIVE_API_VERSION, DATE_FORMAT

firestore_data_bp = Blueprint("database", __name__)


@firestore_data_bp.route(f'{ACTIVE_API_VERSION}stocks_data', methods=['GET'])
def get_historic_data():
    """
    List of ticker data based on passed range

    :return: json of list of data entries
    :rtype: str
    """
    # Check required arguements
    arg_ticker = request.args.get('ticker')
    arg_date_start = request.args.get('date_start')
    arg_date_end = request.args.get('date_end')

    # Validate and convert ticker argument
    v_ticker, ticker = validate_and_convert_args('ticker', arg_ticker, str)  # type: ignore
    if not v_ticker:
        print(ticker)
        abort(400, description={'error': ticker})

    # Validate and convert date_start argument
    v_date_start, date_start = validate_and_convert_args(
        'date_start',
        arg_date_start,  # type: ignore
        datetime,
        datetime.strptime,
        *(arg_date_start, DATE_FORMAT))
    if not v_date_start:
        print(date_start)
        abort(400, description={'error': date_start})

    # Validate and convert date_end argument
    v_date_end, date_end = validate_and_convert_args(
        'date_end',
        arg_date_end,  # type: ignore
        datetime,
        datetime.strptime,
        *(arg_date_end, DATE_FORMAT))
    if not v_date_end:
        abort(400, description={'error': date_end})

    # check if ticker is avail
    if ticker not in db_manager.get_available_tickers():
        abort(404, description={'error': f"ticker {ticker} not found"})

    valid_date_range = validate_date_range(
        date_start, date_end)  # type: ignore
    if not valid_date_range:
        abort(400, description=
              {'error': f"Invalid date ranges, start: {date_start}, end: {date_end}, provided."})

    # retrieve data
    data = db_manager.get_ticker_data(
        ticker, date_start, date_end)  # type: ignore
    return jsonify(data)

@firestore_data_bp.route(f'{ACTIVE_API_VERSION}banner_messages', methods=['GET'])
def get_daily_banner_messages():
    """
    Retrieves randomized (seeded) set of available banner messages

    :return: json of list if messages
    :rtype: str
    """
    messages = db_manager.get_daily_messages()
    # TODO create season and themes for the messages, (Use tags to filter instead of seed)

    # Generate seed using todays date and ip
    date = datetime.utcnow().strftime('%Y-%m-%d')
    ip = request.remote_addr
    if ip:
        # bundle sets of ips for fast hash generation for seed
        # could use geolocation, but want to stay away from using 3rd party libs
        octets = ip.split('.')
        first, last = octets[0], octets[-1]
        seed = f"{date}-{first}-{last}"
    else:
        seed = date
    hashed_seed = hashlib.md5(seed.encode(), usedforsecurity=False).hexdigest()

    print(f"date: {date}, ip: {ip}, seed: {seed}, hashedseed: {hashed_seed}")
    random.seed(hashed_seed)

    # select up to 10 random indices from seed
    num_messages = len(messages)
    random_indices = random.sample(range(num_messages), min(10, num_messages))

    # list comp filtered messages with random indices
    filtered_messages = [messages[i] for i in random_indices]
    return jsonify(filtered_messages)
