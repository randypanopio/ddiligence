#only to be run locally as an admin user DO NOT DEPLOY TO CLOUD LOL
import os
from firebase_admin import initialize_app, firestore, credentials

# Set the path to the service account key JSON file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "super_secrets/serviceAccKey.json"

# Initialize the Firebase Admin SDK with the service account credentials
cred = credentials.Certificate('super_secrets/serviceAccKey.json')
initialize_app(cred)
db = firestore.Client()

from logic.stock_data import get_data
from datetime import datetime, timedelta

"""
    only used to generate base stock data, be careful running this! very expensive lmao
"""

# Iterate over each data entry and add it to Firestore
# TODO standardize json schema somewhere...
ticker = "INTC"
history_start = (datetime.now() - timedelta(days=365.25 * 25)).strftime("%Y-%m-%d")
end = datetime.now().strftime("%Y-%m-%d") 

# for entry in get_data(ticker, history_start, end):
#     doc_ref = db.collection("stocks_data").document(ticker).collection("entries").document(entry["date"])
#     doc_ref.set(entry["data"])

def update_current_tickers():
    print("execution start: " + str(datetime.now()))
    docs = db.collection("stocks_data").stream()
    tickers = [doc.id for doc in docs]
    print(tickers)
    print("execution end: " + str(datetime.now()))

update_current_tickers()
print("complete!")