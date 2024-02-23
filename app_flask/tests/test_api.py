import unittest, os, logging
import api

# unittest requires all test methods to start with test_ !!!!
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

if __name__ == '__main__':
    # Set up logging
    log_file = os.path.join(os.getcwd(), 'test_results.log')
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDebugEndpoints)

    # Run the test suite
    unittest.TextTestRunner().run(suite)