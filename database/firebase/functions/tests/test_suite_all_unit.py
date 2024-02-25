"""
    Test Suite for all current unittests
"""

# import unittest

from logic.tests.test_stock_data import TestGetStockData
from utils.tests.test_utils import TestRetryWrapper

# if __name__ == '__main__':
#     unittest.main()


import unittest

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGetStockData))
    suite.addTest(unittest.makeSuite(TestRetryWrapper))
    suite.addTests(loader.discover('./logic/tests'))
    suite.addTests(loader.discover('utils/tests'))
    # Add more lines like the above to include more directories
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
