"""
    Config and constants
"""
from datetime import datetime
ACTIVE_API_VERSION = '/api/v1/'
DATE_FORMAT = '%Y-%m-%d'
EPOCH_DATE = '1970-01-01' # UNIX time
EPOCH_DATETIME = datetime.strptime(EPOCH_DATE, DATE_FORMAT)

TICKER_COLLECTION = 'ticker_data'
SERIES_COLLECTION = 'entries' #generic name for time series collection
