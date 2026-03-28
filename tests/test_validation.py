import unittest

from numpy.lib._datasource import Repository

from validation.validation import Validation

class TestValidation(unittest.TestCase):

    def setUp(self):
        self.val = Validation()

    def test_valid_coordinates(self):
        self.assertTrue(self.val.validate_coordinates("A1"))
        self.assertTrue(self.val.validate_coordinates("J10"))

    def test_invalid_coordinates(self):
        self.assertFalse(self.val.validate_coordinates("A0"))
        self.assertFalse(self.val.validate_coordinates("K1"))
        self.assertFalse(self.val.validate_coordinates("B20"))
        self.assertFalse(self.val.validate_coordinates("1A"))