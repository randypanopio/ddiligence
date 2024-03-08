# pylint: disable=C0111
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from flask import Flask
from routes.firestore_data import firestore_data_bp


class TestFirestoreDataAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(firestore_data_bp)
        self.client = self.app.test_client()

    @patch('routes.firestore_data.db_manager')
    def test_get_historic_data(self, mock_db_manager):
        mock_db_manager.get_available_tickers.return_value = ['AAPL', 'GOOGL']
        mock_db_manager.get_ticker_data.return_value = [
            {'date': '2023-01-01', 'close_price': 100.0}]

        response = self.client.get(
            '/api/v1/stocks_data?ticker=AAPL&date_start=2023-01-01&date_end=2023-01-01')

        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['date'], '2023-01-01')
        self.assertEqual(data[0]['close_price'], 100.0)

    @patch('routes.firestore_data.db_manager')
    def test_get_daily_banner_messages(self, mock_db_manager):
        mock_db_manager.get_daily_messages.return_value = [
            {'author': 'Author1', 'message': 'Message1', 'tags': ['tag1', 'tag2']},
            {'author': 'Author2', 'message': 'Message2', 'tags': ['tag3', 'tag4']}
        ]
        # TODO figure out mock remote_addr
        response = self.client.get('/api/v1/banner_messages')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        self.assertIn('author', data[0])
        self.assertIn('message', data[0])
        self.assertIn('tags', data[0])


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(TestFireStoreApi))
    unittest.TextTestRunner(verbosity=2).run(suite)
