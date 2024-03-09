'''
    only to be run locally as an admin user DO NOT DEPLOY TO CLOUD LOL
'''
import os
from datetime import datetime, timedelta
import random
from firebase_admin import initialize_app, firestore, credentials
from logic.stock_data import get_data
from main import update_ticker, db, update_current_tickers
from config import *
from unittest.mock import Mock  # Import Mock for testing

# Use and Initialize service account credentials
# SV_PATH = "super_secrets/serviceAccKey.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SV_PATH
# initialize_app(credentials.Certificate(SV_PATH))


def foo():
    """
        only used to generate base stock data, be careful running this! very expensive lmao
        Iterate over each data entry and add it to Firestore
    """
    ticker = "INTC"
    history_start = (datetime.now() -
                     timedelta(days=365.25 * 25)).strftime(DATE_FORMAT)
    end = datetime.now().strftime(DATE_FORMAT)

    for entry in get_data(ticker, history_start, end):
        doc_ref = db.collection("stocks_data").document(
            ticker).collection("entries").document(entry["date"])
        doc_ref.set(entry["data"])



if __name__ == '__main__':
    print("running admin_script")
    from utils.fault_tolerance import retry_wrapper
    day_delta: int = 3
    today = datetime.now()
    start = (today - timedelta(days=day_delta)).strftime(DATE_FORMAT)
    end = today.strftime(DATE_FORMAT)
    tickers = [doc.id for doc in db.collection(TICKER_COLLECTION).stream()]
    def igloo (arg1, arg2, arg3):
        print(f'foo {arg1}, {arg2}, {arg3}')
        if random.random() < 0.5:  # Randomly fails 50% of the time
            raise Exception("Randomly failed")

    for ticker in tickers:
        retry_wrapper(lambda: igloo(ticker, start, end), 5)
    print(f"full execution end: {datetime.now()}")


