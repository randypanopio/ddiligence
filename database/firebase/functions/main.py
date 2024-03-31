'''
    Author: Randy Panopio @rpanopio
'''
import os
from typing import List
from datetime import datetime, timedelta
import yfinance as yf
from firebase_admin import firestore, credentials, initialize_app
from firebase_functions import logger, scheduler_fn

from utils.fault_tolerance import retry_wrapper
from config import DATE_FORMAT, TICKER_COLLECTION, SERIES_COLLECTION

# Use and Initialize service account credentials
SV_PATH = "super_secrets/serviceAccKey.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SV_PATH
initialize_app(credentials.Certificate(SV_PATH))

# Maybe TODO, create a managed class for db connect?
db = firestore.client()

# Maybe TODO expose https_fn endpoint
# @scheduler_fn.on_schedule(
#     schedule="every day 00:00",
#     timezone=scheduler_fn.Timezone("America/Los_Angeles"),
# )  # type: ignore
def update_current_tickers(day_delta: int = 3) -> None:
    """
        updates firebase current tickers with new entries 
        from date of execution and x days from day_delta
    """
    today = datetime.now()
    start = (today - timedelta(days=day_delta)).strftime(DATE_FORMAT)
    end = today.strftime(DATE_FORMAT)
    tickers = [doc.id for doc in db.collection(TICKER_COLLECTION).stream()]
    logger.info(f"execution start: {today}")
    for ticker in tickers:
        retry_wrapper(lambda: update_ticker(ticker, start, end), 5)
    logger.info(f"full execution end: {datetime.now()}")


def update_ticker(ticker: str, start_date: str, end_date: str) -> None:
    """ 
    Retrieves stock data between the start and end date range from yf.
    Saves the data to the connected firestore ticker collection. 

    :param ticker: proper ticker tag EG. AAPL
    :type ticker: str
    :param start_date: YYYY-MM-DD start of date range
    :type start_date: str
    :param end_date: YYYY-MM-DD end of date range
    :type end_date: str
    """
    batch_size = 500
    batch = db.batch()
    sd_doc = db.collection(TICKER_COLLECTION).document(ticker)
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    for i, (date, row) in enumerate(stock_data.iterrows()):
        date_str = date.strftime(DATE_FORMAT)
        date_obj = datetime.strptime(date_str, DATE_FORMAT)
        entry = {
            "Date": date_obj,
            "Open": row["Open"],
            "High": row["High"],
            "Low": row["Low"],
            "Close": row["Close"],
            "Adj Close": row["Adj Close"],
            "Volume": row["Volume"]
        }
        entry_doc = sd_doc.collection(SERIES_COLLECTION).document(date_str)
        batch.set(entry_doc, entry)
        # Check if batch size limit is reached
        if (i + 1) % batch_size == 0:
            batch.commit()
            batch = db.batch()
    # Commit any remaining documents
    batch.commit()

    # update additional metadata
    sd_doc.update({"last_updated": datetime.now(), "source": "yfinance"})
