#only to be run locally as an admin user DO NOT DEPLOY TO CLOUD LOL

# i dunno wtf this does but it fixes my problem about "OSError: Project was not passed and could not be determined from the environment." lol
import os
os.environ.setdefault("GCLOUD_PROJECT", "ddiligence-project")

# The Cloud Functions for Firebase SDK to create Cloud Functions and set up triggers.
from firebase_functions import firestore_fn, https_fn

# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore, credentials
from google.cloud import firestore


from logic.stock_data import get_data
from datetime import datetime, timedelta

cred = credentials.Certificate('super_secrets/serviceAccKey.json')

db = firestore.Client()

initialize_app()

"""
    only used to generate base stock data, be careful running this! very expensive lmao
"""

# Iterate over each data entry and add it to Firestore
# TODO standardize json schema somewhere...
ticker = "INTC"
history_start = (datetime.now() - timedelta(days=365.25 * 25)).strftime("%Y-%m-%d")
end = datetime.now().strftime("%Y-%m-%d") 

for entry in get_data(ticker, history_start, end):
    doc_ref = db.collection("stocks_data").document(ticker).collection("entries").document(entry["date"])
    doc_ref.set(entry["data"])

print("complete!")