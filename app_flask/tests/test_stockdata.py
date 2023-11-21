import unittest
from unittest.mock import patch, mock_open
import stock_data as sd

class TestStockData(unittest.TestCase):

    def test_is_available_existing_stock(self):
        self.assertTrue(sd.is_available("SPY"))

    def test_is_available_nonexisting_stock(self):
        self.assertFalse(sd.is_available("ZZZQQQ"))

    def test_validate_json_valid_schema(self):
        valid_json = {
            "last_updated": "2023-11-16T12:00:00",
            "source": {"name": "", "url": ""},
            "entries": [{"date": "2023-11-15", "data": {"Open": 100, "Close": 110}}]
        }
        self.assertTrue(sd._validate_json(valid_json))

    def test_validate_json_invalid_schema(self):
        invalid_json = {
            "last_updated": "2023-11-16T12:00:00",
            "source": {"name": "", "url": ""},
            "entries": [{"date": "2023-11-15"}]  # Missing required "data" field
        }
        self.assertFalse(sd._validate_json(invalid_json))

    # Assuming SPY data has been generated
    def test_get_existing_stock_data(self):
        stock = "SPY"
        data = sd.get_data(stock)
        # TODO update to be more compreheinsive
        self.assertNotEqual(data, {})

    def test_get_nonexisting_stock_data(self):
        stock = "ZZZQQQ"
        data = sd.get_data(stock)
        self.assertEqual(data, {})

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"last_updated": "2023-01-01T12:00:00", "entries": []}')
    def test_update_data_existing_stock(self, mock_open_file, mock_exists):
        # Test when the stock file exists
        result = sd.update_data("SPY")
        self.assertTrue(result)

    @patch('os.path.exists', return_value=False)
    def test_update_data_non_existing_stock(self, mock_exists):
        # Test when the stock file doesn't exist
        result = sd.update_data("ZZZQQQ")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
