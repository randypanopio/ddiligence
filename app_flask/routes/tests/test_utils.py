# pylint: disable=C0111
"""
    Utils Test Cases
"""
import unittest
from datetime import datetime

from routes.utils import validate_and_convert_args, validate_date_range
from config import DATE_FORMAT


class TestValidateAndConvertArgs(unittest.TestCase):
    def test_successful_conversion_without_function(self):
        result = validate_and_convert_args("arg_name", "10", int)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 10)

    def test_successful_conversion_with_function(self):
        date = "2023-11-21"
        result = validate_and_convert_args(
            "arg_name", date, datetime, datetime.strptime, *(date, DATE_FORMAT)
        )
        self.assertTrue(result[0])
        self.assertEqual(result[1], datetime(2023, 11, 21))

    def test_bad_conversion_suppress_exception(self):
        date = "badedate"
        result = validate_and_convert_args(
            "arg_name", date, datetime, datetime.strptime, *(date, DATE_FORMAT)
        )
        self.assertFalse(result[0])


class TestValidateDateRange(unittest.TestCase):
    def test_valid_date_range(self):
        self.assertTrue(validate_date_range(
            datetime(2023, 11, 20), datetime(2023, 11, 21)))

    def test_invalid_date_ranges(self):
        self.assertFalse(validate_date_range(
            datetime(2023, 11, 22), datetime(2023, 11, 21)))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestValidateAndConvertArgs))
    suite.addTest(unittest.makeSuite(TestValidateDateRange))
    unittest.TextTestRunner(verbosity=2).run(suite)
