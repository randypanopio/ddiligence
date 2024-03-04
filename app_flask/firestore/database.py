'''
    Database Connection class and instance
'''
import os
from typing import List, Tuple
from firebase_admin import firestore, credentials, initialize_app


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
