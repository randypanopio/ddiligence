'''
    Database Connection class and instance
'''
import os
from typing import List
from firebase_admin import firestore, credentials, initialize_app


class DatabaseManager:
    '''
        maybe TODO rewrite for a proper connection handler
        singleton sux... instead should have pool of connection to db and 
        kill connection when it is not in use
    '''
    _instance = None
    sv_path = "super_secrets/serviceAccKey.json"

    def __init__(self) -> None:
        '''
            Initializes database connection
        '''
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.sv_path
        initialize_app(credentials.Certificate(self.sv_path))
        self.db = firestore.client()

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Add methods for database operations as needed, and have routes simply use.
    def get_available_tickers(self) -> List[str]:
        '''
            Retrieves all available tickers from the database, EG. ['INTC', 'AMZN', ...]
        '''
        # Future TODO cache, should have a self ref of this and only update maybe every few hours
        return [doc.id for doc in self.db.collection("stocks_data").stream()]

    # Maybe TODO if there is no free way of retrieving len
    # Cache the len every few hours (then same with seed)
    # if im caching maybe it should be done on a separate thread?
    # Call it background Tasks thread or somn prolly a good idea
    def get_daily_messages(self, indices: List[int]) -> List[(str, str)]:
        '''
            returns tuple of all banner messages available from db
            tup1: author, tup2: message
            TODO cache 
        '''
        doc = self.db.collection('misc').document('banner_messages')
        bar = self.db.collection('misc').order_by('timestamp').offset(5).limit(5)
        # tickers: List[str] = [doc.id for doc in db.collection("stocks_data").stream()]
        # for ticker in tickers:
        #     sd_doc = db.collection("stocks_data").document(ticker)
        #     for entry in get_data(ticker, start_date, end_date):
        #         entry_doc = sd_doc.collection("entries").document(entry["date"])
        #         entry_doc.set(entry["data"]) # set as new entries
        #     sd_doc.update({"last_updated": today, "source": "yfinance"}) # update additional metadata

        return


db_manager = DatabaseManager()
