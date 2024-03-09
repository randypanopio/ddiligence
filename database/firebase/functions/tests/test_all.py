# pylint: disable=C0111, disable=C0413
"""
    Test Suite for all current unittests

    Discovery command:
    python -m unittest discover -s tests -v

    Running unittest discovery of this file only:
    python -m unittest tests/test_all.py -v

    Running this file directly:
    python tests/test_all.py

    generally should use this for testing ensuring coverage
    temporarily comment out functionality that you do not need to test
"""
from utils.tests.test_utils import TestRetryWrapper
from logic.tests.test_stock_data import TestGetStockData
import sys
import os
import unittest
# Add the root directory to enable running this file directly
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)


def routes_suite():
    loader = []
    loader.append(
        unittest.TestLoader().loadTestsFromTestCase(TestGetStockData))
    loader.append(
        unittest.TestLoader().loadTestsFromTestCase(TestRetryWrapper))
    return loader


if __name__ == '__main__':
    primary_suite = unittest.TestSuite()
    primary_suite.addTests(routes_suite())
    runner = unittest.TextTestRunner(verbosity=2)

    runner.run(primary_suite)
    # runner.run(local_suite()) # use me and supress above when running custom local test suites
