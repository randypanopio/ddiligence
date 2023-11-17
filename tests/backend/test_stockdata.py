import unittest, json
import pandas as pd
from io import StringIO
from unittest.mock import patch, mock_open
from app_flask.stock_data import update_data, get_data

class TestDataFunctions(unittest.TestCase):
    def setUp(self):
        pass

    @patch('yfinance.download')
    @patch('builtins.open', create=True)
    def test_update_data(self, mock_open, mock_yfinance):
        # Mock data for the yfinance download
        df_raw = """
        Date,Open,High,Low,Close,Adj Close,Volume
        2023-01-03,243.080002,245.750000,237.399994,239.580002,237.956329,25740000
        2023-01-04,232.279999,232.869995,225.960007,229.100006,227.547348,50623400
        """
        mock_yfinance.return_value = pd.read_csv(StringIO(df_raw), parse_dates=True, index_col=0)

        # Call the update_data function
        result = update_data("SPY")

        # Assert that the function returned True (indicating successful update)
        self.assertTrue(result)

        # Mock assertions to check if open was called correctly
        mock_open.assert_called_with('data/stocks/SPY_data.json', 'w')
        mock_open.return_value.__enter__.return_value.write.assert_called()

    @patch('builtins.open', new_callable=mock_open, read_data='{"last_updated": "2023-11-09T22:12:17", "data": {"2023-01-03": {"data": {"Open": 243.0800018310547, "High": 245.75, "Low": 237.39999389648438, "Close": 239.5800018310547, "Adj Close": 237.9563446044922, "Volume": 25740000.0}}}}')
    def test_get_data_returns_data(self, mock_open):
        # mock file open and read
        result = get_data("SPY")

        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main()
