'''
    Author: Randy Panopio @rpanopio
'''
import os
from typing import List
from datetime import datetime, timedelta
from firebase_admin import firestore, credentials, initialize_app
from firebase_functions import logger, scheduler_fn

from logic.stock_data import get_data
from utils.fault_tolerance import retry_wrapper

# Use and Initialize service account credentials
SV_PATH = "super_secrets/serviceAccKey.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SV_PATH
initialize_app(credentials.Certificate(SV_PATH))

# Maybe TODO, create single db connection, esp when creating multiple gfuncs?
db = firestore.client()

# Maybe TODO expose https_fn endpoint
@scheduler_fn.on_schedule(
    schedule="every day 00:00",
    timezone=scheduler_fn.Timezone("America/Los_Angeles"),
)
def update_current_tickers(day_delta: int = 3) -> None:
    """
        updates firebase current tickers with new entries 
        from date of execution and x days from day_delta
    """
    today = datetime.now()
    logger.info(f"execution start: {today}")

    def update():
        start_date: str = (today - timedelta(days=day_delta)
                           ).strftime("%Y-%m-%d")
        end_date: str = today.strftime("%Y-%m-%d")

        tickers: List[str] = [
            doc.id for doc in db.collection("stocks_data").stream()]
        for ticker in tickers:
            sd_doc = db.collection("stocks_data").document(ticker)
            for entry in get_data(ticker, start_date, end_date):
                entry_doc = sd_doc.collection(
                    "entries").document(entry["date"])
                entry_doc.set(entry["data"])  # set as new entries
            # update additional metadata
            sd_doc.update({"last_updated": today, "source": "yfinance"})

    retry_wrapper(update, 5)
    logger.info(f"full execution end: {datetime.now()}")
