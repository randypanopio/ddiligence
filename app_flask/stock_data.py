import json, os
import jsonschema
from datetime import datetime, timedelta
import yfinance as yf
from data_validation import history_start, base_json_schema

available_stocks = {"SPY", "MSFT"}

def is_available(ticker):
    if isinstance(ticker, str) and ticker.strip():  # Check if it's a non-empty string
        ticker_upper = ticker.upper()  # Convert to uppercase
        return ticker_upper in available_stocks
    return False


def _validate_json(json_data):
    try:
        jsonschema.validate(instance=json_data, schema=json.loads(base_json_schema))
        print('Valid Json Schema')
        return True
    except jsonschema.ValidationError as e:
        print("Json Schema Validation Error:")
        print(e)
        return False


# yfinance for nowsies:
#TODO migrate to a proper db solution, using json files for proof of concept
def update_data(ticker):
    '''
        Update the historic data of the ticker.
        returns True if new data was retrieved and stored
    '''
    if not is_available(ticker):
        print(f"{ticker} is not available or is empty.")
        return False
    else:
        file_path = f'data/stocks/{ticker}_data.json'
        try:
            # Check if the file exists
            if os.path.exists(file_path):
                # Load existing JSON data
                print(f'file {file_path} exists proceeding')
                with open(file_path, 'r') as existing_file:
                    existing_data = json.load(existing_file)
                    print(f"succesfully read {file_path} file")

                # Check the last_updated timestamp
                # NOTE probably slow due to having to deserialize the whole json file, but for now we leave it alone :)
                last_updated_str = existing_data.get("last_updated", "")
                last_updated = datetime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%S") if last_updated_str else datetime.min

                print("rate limit step")
                # Check if the data is updated within the last hour
                rate_limit_seconds = 60
                if datetime.now() - last_updated < timedelta(seconds=rate_limit_seconds):
                    print(f"Data for {ticker} was updated less than an {rate_limit_seconds} seconds ago. Skipping update.")
                    return False
            else:
                print(f'file {file_path} has not been generated')

            # Download new stock data, maybe TODO, include a validation
            stock_data = yf.download(ticker, start=history_start, end=datetime.now().strftime("%Y-%m-%d"))

            # TODO since storing timestamp in file, it doesnt make sense create a store_data function, but deff need to make one when changing to proper db solution
            # add last update and the historic data into one json and save to file
            new_update_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            stock_data_entries = []
            for date, row in stock_data.iterrows():
                date_str = date.strftime("%Y-%m-%d")
                entry = {
                    "date": date_str,
                    "data": {
                        "Open": row["Open"],
                        "High": row["High"],
                        "Low": row["Low"],
                        "Close": row["Close"],
                        "Adj Close": row["Adj Close"],
                        "Volume": row["Volume"]
                    }
                }
                stock_data_entries.append(entry)

            data_wrapped = {
                "last_updated": new_update_time,
                "source": {"name": "yfinance", "url": ""},
                "entries": stock_data_entries
            }
            stock_data_json = json.dumps(data_wrapped, indent=2)

            # NOTE since I am already manually authoring how i save my json, i shouldnt need validation
            # TODO update instead to generate my json from my schema? Maybe when I expand and include a lot of data sets i wont know their schema, then i should
            if _validate_json(data_wrapped):
                with open(file_path, 'w') as f:
                    f.write(stock_data_json)
                    print(f"Data for {ticker} updated successfully.")
                return True
            else:
                print(f"Invalid json schema")
                return False
        except Exception as e:
            print(f"Failed to update {ticker} data.")
            print(e)
            return False


def get_data(ticker):
    if not isinstance(ticker, str) or not ticker.strip():
        print("No valid ticker passed.")
        return {}
    ticker_u = ticker.upper()
    if ticker_u not in available_stocks:
        print(ticker_u + " is not available")
        return {}
    else:
        try:
            file_path = 'data/stocks/{0}_data.json'.format(ticker_u)
            with open(file_path, 'r') as f:
                content = json.load(f)
                # TODO for now its fine to return the entire json, but likely will change in the future.
                return content
        except Exception as e:
            print(f"Failed to retrieve {ticker_u} historic data.")
            print(e)
            return {}