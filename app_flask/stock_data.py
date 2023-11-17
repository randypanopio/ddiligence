import json, os
import jsonschema
from datetime import datetime, timedelta
import yfinance as yf

available_stocks = {"SPY", "MSFT"}

# NOTE ensure json schema is valid DURING storage of data, and not retrieval

# YYYY-MM-DD limit our hist data for up to 25 yrs
history_start = (datetime.now() - timedelta(days=365.25 * 25)).strftime("%Y-%m-%d")


schema = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "last_updated": {"type": "string", "format": "date-time"},
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "date": {"type": "string", "format": "date"},
          "data": {"type": "object"}
        },
        "required": ["date", "data"]
      }
    }
  },
  "required": ["last_updated", "entries"]
}
"""

def _validate_json(json_data):
    try:
        jsonschema.validate(instance=json_data, schema=json.loads(schema))
        return True
    except jsonschema.ValidationError as e:
        print("Validation Error:")
        print(e)
        return False


# yfinance for nowsies:
#TODO migrate to a proper db solution, using json files for proof of concept
def update_data(ticker):
    '''
        Cache the historic data of the ticker.
        returns True if new data was retrieved and stored
    '''
    if ticker not in available_stocks:
        print(ticker + " is not available")
        return False
    else:
        file_path = 'data/stocks/{0}_data.json'.format(ticker)

        try:
            # Check if the file exists
            if os.path.exists(file_path):
                # Load existing JSON data
                with open(file_path, 'r') as existing_file:
                    existing_data = json.load(existing_file)

                # Check the last_updated timestamp
                # NOTE probably slow due to having to deserialize the whole json file, but for now we leave it alone :)
                last_updated_str = existing_data.get("last_updated", "")
                last_updated = datetime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%S") if last_updated_str else datetime.min

                # Check if the data is updated within the last hour
                rate_limit_seconds = 60
                if datetime.now() - last_updated < timedelta(seconds=rate_limit_seconds):
                    print(f"Data for {ticker} was updated less than an {rate_limit_seconds} seconds ago. Skipping update.")
                    return False

            # Download new stock data, maybe TODO, include a validation
            stock_data = yf.download(ticker, start=history_start, end=datetime.now().strftime("%Y-%m-%d"))

            # TODO since storing timestamp in file, it doesnt make sense create a store_data function, but deff need to make one when changing to proper db solution
            # add last update and the historic data into one json and save to file
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

            new_update_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            data_wrapped = {"last_updated": new_update_time, "entries": stock_data_entries}
            stock_data_json = json.dumps(data_wrapped, indent=2)

            # NOTE since I am already manually authoring how i save my json, i shouldnt need validation
            # TODO update instead to generate my json from my schema? Maybe when I expand and include a lot of data sets i wont know their schema, then i should
            if _validate_json(data_wrapped):
                stock_data_json = json.dumps(data_wrapped, indent=2)
                with open(file_path, 'w') as f:
                    f.write(stock_data_json)
                print(f"Data for {ticker} updated successfully.")
                return True
            else:
                print(f"Invalid json schema")
                return False
        except Exception as e:
            print("Failed to update data.")
            print(e)
            return False


def get_data(ticker):
    file_path = 'data/stocks/{0}_data.json'.format(ticker)
    if ticker not in available_stocks:
        print(ticker + " is not available")
        return {}
    else:
        try:
            with open(file_path, 'r') as f:
                content = json.load(f)
                # get data only
                historic_data = content.get("data", {})
                return historic_data
        except Exception as e:
            print(f"Failed to retrieve historic data for {ticker}.")
            print(e)
            return {}

if __name__ == '__main__':
    stock = "SPY"
    update_data(stock)
    get_data(stock)