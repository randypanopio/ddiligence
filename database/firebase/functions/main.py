import os
from datetime import datetime, timedelta
from firebase_admin import initialize_app, firestore, credentials
from firebase_functions import logger, https_fn, options
from logic.stock_data import get_data
from typing import List

# Set the path to the service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "super_secrets/serviceAccKey.json"
# Initialize the Firebase Admin SDK with the service account credentials
cred = credentials.Certificate('super_secrets/serviceAccKey.json')
initialize_app(cred)
db = firestore.Client()

def update_current_tickers(day_delta: int = 3):
    """
        updates firebase current tickers with new entries from date of execution and x days from day_delta
    """  
    today = datetime.now()
    logger.info("execution start: {0}".format(str(today)))
    
    start_date: str = (today - timedelta(days=day_delta)).strftime("%Y-%m-%d") 
    end_date: str = today.strftime("%Y-%m-%d")
    
    tickers: List[str] = [doc.id for doc in db.collection("stocks_data").stream()]
    for ticker in tickers:
        sd_doc = db.collection("stocks_data").document(ticker)
        for entry in get_data(ticker, start_date, end_date):
            entry_doc = sd_doc.collection("entries").document(entry["date"])
            entry_doc.set(entry["data"]) # set as new entries
        sd_doc.update({"last_updated": today, "source": "yfinance"}) # update additional metadata

    logger.info("execution end: " + str(datetime.now()))
