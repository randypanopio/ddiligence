'''
    Database Connection class and instance
'''
import os
import json
from typing import List, Tuple, Any
from datetime import datetime
from firebase_admin import firestore, credentials, initialize_app
from config import TICKER_COLLECTION, SERIES_COLLECTION


class DatabaseManager:
    '''
        maybe TODO rewrite for a proper connection handler
        singleton sux... instead should have pool of connection to db and 
        kill connection when it is not in use

        Actually TODO, implement caching
    '''
    _instance = None

    def __init__(self) -> None:
        '''
            Initializes database connection
        '''
        # check if local file (eg local dev) and set as env var
        # set it as an env var and init app with this credentials
        # otherwise it will get env EG. on GitHub Actions - use secret env vars
        sv_path = "super_secrets/serviceAccKey.json"
        if os.path.exists(sv_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sv_path
            initialize_app(credentials.Certificate(sv_path))
        else:
            env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            initialize_app(credentials.Certificate(json.loads(env))) # type: ignore

        self.db = firestore.client()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_available_tickers(self) -> List[str]:
        """
        Retrieves all available tickers from the database
        :return: EG. ['INTC', 'AMZN', ...]
        :rtype: List[str]
        """
        # Future TODO cache, should have a self ref of this and only update maybe every few hours
        return [doc.id for doc in self.db.collection(TICKER_COLLECTION).stream()]

    def get_ticker_data(self, ticker: str, date_start: datetime, date_end: datetime) -> List[Any]:
        """
        Gets all available data from the passed ticker
        given the passed date range  

        :param ticker: proper ticker EG. AAPL
        :type ticker: str
        :param date_start: date range start
        :type date_start: datetime
        :param date_end: date range end
        :type date_end: datetime
        :return: list of ticker data
        :rtype: List[Any]
        """
        # TODO normalize date range, EG convert from whatever UTC to day 0?
        # probably TODO, reason why we dont query db directly is to cache on server

        ref = self.db.collection(TICKER_COLLECTION).document(
            ticker).collection(SERIES_COLLECTION)
        # Construct the query, filtering by the date range
        query = ref.where("Date", ">=", date_start) \
            .where("Date", "<=", date_end)
        # convert to a seriazible type
        return self._format_stream(query.stream())

    # TODO cache the daily messages every few hours

    def get_daily_messages(self) -> List[Tuple[str, str, List[str]]]:
        """_summary_
        list of all banner messages available from db
        :return: returns list of tuples containing (author, message, tags) 
        :rtype: List[Tuple[str, str, List[str]]]
        """
        messages = []
        for doc in self.db.collection('banner_messages').get():
            data = doc.to_dict()  # Convert the document to a Python dictionary
            author = data.get('author', '')  # Get the author field
            message = data.get('message', '')  # Get the message field
            tags = data.get('tags', [])  # Get the tags field

            messages.append((author, message, tags))
        return messages

    def _format_stream(self, struct):
        data = []
        for d in struct:
            data.append(d.to_dict())
        return data


db_manager = DatabaseManager()
