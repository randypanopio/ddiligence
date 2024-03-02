import os
from typing import List
from firebase_admin import firestore, credentials, initialize_app

class DatabaseManager:
    """
        maybe TODO rewrite for a proper connection handler
        singleton sux... instead should have pool of connection to db and 
        kill connection when it is not in use
    """
    _instance = None
    sv_path = "super_secrets/serviceAccKey.json"

    def __init__(self) -> None:
        """
            Initializes database connection
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.sv_path
        initialize_app(credentials.Certificate(self.sv_path))
        self.db = firestore.client()

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Add methods for database operations as needed, and have routes simply use.
    def get_available_tickers(self) -> List[str]:
        """
            Retrieves all available tickers from the database, EG. ['INTC', 'AMZN', ...]
        """
        # TODO cache, should have a self ref of this and only update maybe every few hours
        print("bar")
        res = [doc.id for doc in self.db.collection("stocks_data").stream()]
        for var in res:
            print(var)
        return res

db_manager = DatabaseManager()
