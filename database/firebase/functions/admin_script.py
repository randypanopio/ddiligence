'''
    only to be run locally as an admin user DO NOT DEPLOY TO CLOUD LOL
'''
import os
from datetime import datetime, timedelta
from firebase_admin import initialize_app, firestore, credentials
from logic.stock_data import get_data

# Use and Initialize service account credentials
SV_PATH = "super_secrets/serviceAccKey.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SV_PATH
initialize_app(credentials.Certificate(SV_PATH))

db = firestore.client() # create own db connect

def update_ticker():
    """
        only used to generate base stock data, be careful running this! very expensive lmao
        Iterate over each data entry and add it to Firestore
    """
    ticker = "INTC"
    history_start = (datetime.now() -
                     timedelta(days=365.25 * 25)).strftime("%Y-%m-%d")
    end = datetime.now().strftime("%Y-%m-%d")

    for entry in get_data(ticker, history_start, end):
        doc_ref = db.collection("stocks_data").document(
            ticker).collection("entries").document(entry["date"])
        doc_ref.set(entry["data"])

# update_ticker()
print("complete!")
