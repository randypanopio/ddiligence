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
import sys
import os
import unittest
# Add the root directory to enable running this file directly
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from routes.tests.test_utils import TestValidateAndConvertArgs, TestValidateDateRange
from routes.tests.test_firestore_data import TestFirestoreDataAPI

def routes_suite():
    loader = []
    loader.append(unittest.TestLoader(
    ).loadTestsFromTestCase(TestFirestoreDataAPI))
    loader.append(unittest.TestLoader().loadTestsFromTestCase(
        TestValidateAndConvertArgs))
    loader.append(unittest.TestLoader().loadTestsFromTestCase(
        TestValidateDateRange))
    return loader


def local_suite():
    """
    Use me when running custom local test suites
    """
    suite = unittest.TestSuite()
    # Add runners here
    # EG: suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFirestoreDataAPI))
    return suite


if __name__ == '__main__':
    primary_suite = unittest.TestSuite()
    primary_suite.addTests(routes_suite())
    runner = unittest.TextTestRunner(verbosity=2)

    runner.run(primary_suite)
    # runner.run(local_suite()) # use me and supress above when running custom local test suites
