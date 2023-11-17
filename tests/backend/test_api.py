import unittest, os, logging

from app_flask.api import app


class TestDebugEndpoints(unittest.TestCase):
    def setUp(self):
        # Create a test client to simulate HTTP requests
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_status_code(self):
        response = self.app.get('/api/hello')
        self.assertEqual(response.status_code, 200)

    def test_hello_response(self):
        response = self.app.get('/api/hello')
        data = response.get_json()
        self.assertEqual(data, {'message': 'Hello'})


if __name__ == '__main__':
    # Set up logging
    log_file = os.path.join(os.getcwd(), 'test_results.log')
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDebugEndpoints)

    # Run the test suite
    unittest.TextTestRunner().run(suite)