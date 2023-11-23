import unittest, os, logging
import api

class TestDebugEndpoints(unittest.TestCase):
    def setUp(self):
        self.version_prefix = '/api/v1/'
        self.app = api.app.test_client()
        self.app.testing = True

    def test_hello_status_code(self):
        response = self.app.get(f'{self.version_prefix}hello')
        self.assertEqual(response.status_code, 200)

    def test_hello_response(self):
        response = self.app.get(f'{self.version_prefix}hello')
        data = response.get_json()
        expected_message = {'message': f'{self.version_prefix} API is available'}
        self.assertEqual(data, expected_message)

    def test_stock_history_nonexistent(self):
        response = self.app.get(f'{self.version_prefix}stock_history?ticker=ZZZQQQ')
        self.assertEqual(response.status_code, 404)
        # TODO extend handle abort obj (its not in response) and match valid message

    def test_stock_history(self):
        response = self.app.get(f'{self.version_prefix}stock_history?ticker=SPY')
        data = response.get_json()
        self.assertIn('entries', data)
        self.assertIsInstance(data['entries'], list)
        self.assertGreater(len(data['entries']), 0)
        for entry in data['entries']:
            self.assertIsInstance(entry, dict)

    def test_DEBUG(self):
        self.assertEqual(1,2)


if __name__ == '__main__':
    # Set up logging
    log_file = os.path.join(os.getcwd(), 'test_results.log')
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDebugEndpoints)

    # Run the test suite
    unittest.TextTestRunner().run(suite)