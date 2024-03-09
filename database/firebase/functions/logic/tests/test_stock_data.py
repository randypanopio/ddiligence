# pylint: disable=C0111, disable=C0413
import unittest
import pandas as pd
from datetime import datetime
from unittest.mock import patch
from logic.stock_data import get_data


class TestGetStockData(unittest.TestCase):
    @patch('logic.stock_data.yf.download')
    def test_get_data(self, mock_download):
        # Set up mock data for yf.download
        mock_data = {
            'Open': [100.0, 101.0],
            'High': [105.0, 106.0],
            'Low': [98.0, 99.0],
            'Close': [102.0, 103.0],
            'Adj Close': [102.0, 103.0],
            'Volume': [1000000, 2000000]
        }
        mock_dataframe = pd.DataFrame(mock_data)
        mock_dataframe.index = pd.to_datetime(['2023-01-01', '2023-01-02'])
        mock_download.return_value = mock_dataframe

        # Call the get_data function with mock parameters
        ticker = 'INTC'
        start = '2023-01-01'
        end = '2023-01-02'
        result = get_data(ticker, start, end)

        # Expected result based on mock data
        expected_result = [
            {
                "date": "2023-01-01",
                "Open": 100.0,
                "High": 105.0,
                "Low": 98.0,
                "Close": 102.0,
                "Adj Close": 102.0,
                "Volume": 1000000
            },
            {
                "date": "2023-01-02",
                "Open": 101.0,
                "High": 106.0,
                "Low": 99.0,
                "Close": 103.0,
                "Adj Close": 103.0,
                "Volume": 2000000
            }
        ]

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGetStockData))
    unittest.TextTestRunner(verbosity=2).run(suite)