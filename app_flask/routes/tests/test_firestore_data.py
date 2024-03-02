import unittest, os, logging
from unittest.mock import patch
from firestore.database import db_manager

class TestFireStoreApi(unittest.TestCase):

    def test_foo(self):
        print("foo")
        db_manager.get_available_tickers()

if __name__ == '__main__':
    # Set up logging
    log_file = os.path.join(os.getcwd(), 'test_results.log')
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFireStoreApi)

    # Run the test suite
    unittest.TextTestRunner().run(suite)        