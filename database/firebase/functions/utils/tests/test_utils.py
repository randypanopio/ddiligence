import unittest, os, logging
from unittest.mock import MagicMock
from utils.fault_tolerance import retry_wrapper

class TestRetryWrapper(unittest.TestCase):
    def test_retry_wrapper_success(self):
        # Define a mock function that succeeds after a few retries
        mock_function = MagicMock()
        mock_function.side_effect = [Exception(), Exception(), 'Success']

        # Call the retry_wrapper with the mock function
        result = retry_wrapper(mock_function, max_retries=3, base_delay=1, max_delay=5)

        # Assert that the result is 'Success'
        self.assertEqual(result, 'Success')        

        # Assert that the mock function was called three times
        self.assertEqual(mock_function.call_count, 3)

    def retry_wrapper_failure(self):
        # Define a mock function that always raises an exception
        mock_function = MagicMock(side_effect=Exception('Function failed'))

        # Call the retry_wrapper with the mock function
        with self.assertRaises(Exception) as context:
            retry_wrapper(mock_function, max_retries=3, base_delay=1, max_delay=5)

        # Assert that the expected exception was raised
        self.assertEqual(str(context.exception), 'Max retries reached. Operation failed.')

        # Assert that the mock function was called three times
        self.assertEqual(mock_function.call_count, 3)

if __name__ == '__main__':
    # Set up logging
    log_file = os.path.join(os.getcwd(), 'test_results.log')
    logging.basicConfig(filename=log_file, level=logging.INFO)

    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRetryWrapper)

    # Run the test suite
    unittest.TextTestRunner().run(suite)
