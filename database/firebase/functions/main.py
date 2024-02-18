import os
from datetime import datetime, timedelta
from firebase_admin import initialize_app, firestore, credentials
from logic.stock_data import get_data
from typing import List

# Set the path to the service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "super_secrets/serviceAccKey.json"
# Initialize the Firebase Admin SDK with the service account credentials
cred = credentials.Certificate('super_secrets/serviceAccKey.json')
initialize_app(cred)
db = firestore.Client()

# daily function to update db with new data
tickers = ["AAPL", "ADBE", "AMZN", "CSCO", "GOOG", "GOOGL", "INTC", "META", "MSFT", "NFLX"]

def get_latest(tickers: List[str], day_delta: int):
    """
        TODO write me
    """
    start = (datetime.now() - timedelta(days=day_delta)).strftime("%Y-%m-%d") 
    end = datetime.now().strftime("%Y-%m-%d") 
    print("execution start: " + str(datetime.now()))
    for ticker in tickers:
        sd_doc = db.collection("stocks_data").document(ticker)
        for entry in get_data(ticker, start, end):
            entry_doc = sd_doc.collection("entries").document(entry["date"])
            entry_doc.set(entry["data"])
        sd_doc.set({"last_updated": datetime.now()})
        sd_doc.set({"source" : "yfinance"})
        break
    print("completed at: " + str(datetime.now()))

# run daily update
get_latest(tickers, 3)