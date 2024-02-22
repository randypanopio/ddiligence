import os
from datetime import datetime, timedelta
from firebase_admin import initialize_app, firestore, credentials
from firebase_functions import logger, https_fn, options
from typing import List

from logic.stock_data import get_data
from fault_utils import retry_wrapper

# Use and Initialize service account credentials
sv_path = "super_secrets/serviceAccKey.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sv_path
initialize_app(credentials.Certificate(sv_path))

db = firestore.Client()

def update_current_tickers(day_delta: int = 3) -> None:
    """
        updates firebase current tickers with new entries from date of execution and x days from day_delta
    """  
    today = datetime.now()
    logger.info("execution start: {0}".format(str(today)))

    def update():
        start_date: str = (today - timedelta(days=day_delta)).strftime("%Y-%m-%d") 
        end_date: str = today.strftime("%Y-%m-%d")
        
        tickers: List[str] = [doc.id for doc in db.collection("stocks_data").stream()]
        for ticker in tickers:
            sd_doc = db.collection("stocks_data").document(ticker)
            for entry in get_data(ticker, start_date, end_date):
                entry_doc = sd_doc.collection("entries").document(entry["date"])
                entry_doc.set(entry["data"]) # set as new entries
            sd_doc.update({"last_updated": today, "source": "yfinance"}) # update additional metadata

    retry_wrapper(update, 5)
    logger.info("full execution end: {0}".format(str(datetime.now())))