'''
    Database Connection class and instance
'''
import os
from sqlite3 import Timestamp
from typing import List, Tuple
from datetime import datetime
from firebase_admin import firestore, credentials, initialize_app
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
# from firebase 


class DatabaseManager:
    '''
        maybe TODO rewrite for a proper connection handler
        singleton sux... instead should have pool of connection to db and 
        kill connection when it is not in use

        Actually TODO, implement caching
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

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_available_tickers(self) -> List[str]:
        '''
            Retrieves all available tickers from the database, EG. ['INTC', 'AMZN', ...]
        '''
        # Future TODO cache, should have a self ref of this and only update maybe every few hours
        return [doc.id for doc in self.db.collection("stocks_data").stream()]

    def get_ticker_data(self, ticker: str, date_start: datetime, date_end: datetime):
        # Convert datetime objects to strings (YYYY-MM-DD format)
        start_timestamp_str = date_start.strftime("%Y-%m-%d")
        end_timestamp_str = date_end.strftime("%Y-%m-%d")

        # Access the collection and subcollections
        stock_data_ref = self.db.collection('stocks_data').document(ticker).collection('entries')

        # Construct the query with string comparisons for date range (using string values directly for comparison)
        # query_results = stock_data_ref.where("__name__", ">=", start_timestamp_str) \
        #                         .where("__name__", "<=", end_timestamp_str)
        # query = stock_data_ref.where(FieldPath.document_id(), '>=', start_timestamp_str)
        # query = self.db.collection('stocks_data').document(ticker).collection('entries').where(FieldPath.document_id(), '>=', start_timestamp_str).get()
        # query_results = stock_data_ref.where(FieldPath.document_id(), ">=", start_timestamp_str) \
        #                  .where(FieldPath.document_id(), "<=", end_timestamp_str)

        print(FieldPath.document_id())
        # Stream or get results as needed
        data = []
        # for doc in query:
        #     data.append(doc.to_dict())
        return data

    # def get_ticker_data(self, ticker: str,
    #                     date_start: datetime, date_end: datetime
    #                     ): # TODO type annotate
    #     # Convert datetime objects to Firestore Timestamps
    #     start_timestamp = "2024-01-31" # TEMP HARD CODED
    #     end_timestamp = "2024-03-23"

    #     stock_data_ref = self.db.collection('stocks_data').document(ticker).collection('entries')
    #     start_timestamp = "2024-01-31" # this gets changed but I need to find document by this id
    #     query_results = stock_data_ref.where(FieldPath('__name__'), '>=', start_timestamp)
        
    #     # Extract queried data
    #     data = []
    #     for doc in query_results.stream(): # query_results
    #         data.append(doc.to_dict())
    #     return data
        # # Query Firestore subcollection
        # # doc_id = FieldPath.documentId()
        # # sd_ref = self.db.collection('stocks_data').document(ticker).collection('entries')
        # # query = sd_ref.where(filter=FieldFilter("capital", "==", True))
        # # # query = stock_data_ref.order_by(FieldPath.document_id()).start_at(date_start).end_at(date_end) #.where('date', '>=', date_start).where('date', '<=', date_end)
        # # query_results = query.stream()

        # # # Extract queried data
        # # data = []
        # # for doc in query_results:
        # #     data.append(doc.to_dict())
        #     # Query Firestore subcollection
        # stock_data_ref = self.db.collection('stocks_data').document(ticker).collection('entries')
        # query = stock_data_ref.where('__name__', '>=', date_start).where('__name__', '<=', date_end)
        # query_results = query.stream()

        # # Extract queried data
        # data = []
        # for doc in query_results:
        #     data.append(doc.to_dict())
        # return data

    # TODO cache the daily messages every few hours

    def get_daily_messages(self) -> List[Tuple[str, str, List[str]]]:
        '''
            returns list of tuples containing (author, message, tags) 
            for all banner messages available from db
        '''
        messages = []
        for doc in self.db.collection('banner_messages').get():
            data = doc.to_dict()  # Convert the document to a Python dictionary
            author = data.get('author', '')  # Get the author field
            message = data.get('message', '')  # Get the message field
            tags = data.get('tags', [])  # Get the tags field

            messages.append((author, message, tags))
        return messages


db_manager = DatabaseManager()

# if __name__ == '__main__':
#     ticker = 'UBER'
#     format = "%Y-%m-%d"
#     d1 = "2024-01-31"
#     d2 = "2024-02-23"
#     date1 = datetime.strptime(d1, format)
#     date2 = datetime.strptime(d1, format)
#     data = db_manager.get_ticker_data(ticker, date1, date2) # type: ignore
#     # print(validate_date_range(date1, date2)) # type: ignore
#     for d in data: # type: ignore
#         print(d)