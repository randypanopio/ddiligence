import unittest, os, logging
import pandas as pd
from datetime import datetime
from unittest.mock import patch
from datetime import datetime
from logic.stock_data import get_data

class TestGetStockData(unittest.TestCase):
    @patch('logic.stock_data.yf.download')
    def test_get_data(self, mock_download):
        # all this to mock yf DF 
        mock_data = {
            'Open': [44.259998, 44.480000, 44.680000, 43.130001],
            'High': [45.169998, 44.689999, 44.680000, 43.509998],
            'Low': [43.419998, 43.080002, 42.529999, 42.660000],
            'Close': [44.520000, 43.470001, 42.980000, 42.990002],
            'Adj Close': [44.520000, 43.470001, 42.980000, 42.990002],
            'Volume': [61514100, 57715000, 62809300, 33779200]
        }

        dates = ['2024-02-20', '2024-02-21', '2024-02-22', '2024-02-23']
        date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        mock_dataframe = pd.DataFrame(mock_data, index=date_objects)
        mock_download.return_value = mock_dataframe

        # Call the get_data function with mock parameters
        ticker = 'INTC'
        start = datetime(2024, 2, 20)
        end = datetime(2024, 2, 23)
        result = get_data(ticker, start, end)

        # fromatted json obj we actually use 
        expected_result = [{"date":"2024-02-20","data":{"Open":44.259998,"High":45.169998,"Low":43.419998,"Close":44.52,"Adj Close":44.52,"Volume":61514100}},{"date":"2024-02-21","data":{"Open":44.48,"High":44.689999,"Low":43.080002,"Close":43.470001,"Adj Close":43.470001,"Volume":57715000}},{"date":"2024-02-22","data":{"Open":44.68,"High":44.68,"Low":42.529999,"Close":42.98,"Adj Close":42.98,"Volume":62809300}},{"date":"2024-02-23","data":{"Open":43.130001,"High":43.509998,"Low":42.66,"Close":42.990002,"Adj Close":42.990002,"Volume":33779200}}]

        # Assert that the result matches the expected result
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    # Set up logging
    log_file = os.path.join(os.getcwd(), 'test_results.log')
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGetStockData)

    # Run the test suite
    unittest.TextTestRunner().run(suite)
