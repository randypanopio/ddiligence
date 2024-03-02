"""
    Test Suite for all current unittests
"""
import unittest
from routes.tests.test_firestore_data import TestFireStoreApi

def suites():
    """TODO docstring"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFireStoreApi))
    suite.addTests(loader.discover('./routes/tests'))
    # Add more lines like the above to include more directories
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suites())
