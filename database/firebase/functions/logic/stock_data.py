'''
    Retrieves ticker data using yfinance library
'''
import yfinance as yf

def get_data(ticker: str, start: str, end: str):
    '''
        Returns json object of historic data of passed ticker

        start:
            datetime string
        end:
            datetime string
    '''
    ticker = ticker.upper()
    # TODO add validation but dunno how it works really
    stock_data = yf.download(ticker, start=start, end=end)
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
    return stock_data_entries
