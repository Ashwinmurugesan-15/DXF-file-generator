import unittest
import sys
import os
from unittest.mock import patch
import io

# Add the project root to the sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.interfaces.validator import Validator

class TestValidator(unittest.TestCase):

    def test_validate_float_valid(self):
        rule = {'min': 10, 'max': 100, 'description': 'Test Value'}
        self.assertTrue(Validator._validate_float(50, rule)[0])
        self.assertTrue(Validator._validate_float(10, rule)[0])
        self.assertTrue(Validator._validate_float(100, rule)[0])

    def test_validate_float_out_of_range(self):
        rule = {'min': 10, 'max': 100, 'description': 'Test Value'}
        self.assertFalse(Validator._validate_float(5, rule)[0])
        self.assertFalse(Validator._validate_float(105, rule)[0])
        self.assertEqual(Validator._validate_float(5, rule)[1], "Error: Test Value must be between 10 and 100 mm.")
        self.assertEqual(Validator._validate_float(105, rule)[1], "Error: Test Value must be between 10 and 100 mm.")

    def test_validate_float_non_numeric(self):
        rule = {'min': 10, 'max': 100, 'description': 'Test Value'}
        self.assertFalse(Validator._validate_float("abc", rule)[0])
        self.assertEqual(Validator._validate_float("abc", rule)[1], "Error: Test Value must be a number.")
        self.assertFalse(Validator._validate_float(None, rule)[0])
        self.assertEqual(Validator._validate_float(None, rule)[1], "Error: Test Value must be a number.")

    def test_validate_beam_valid(self):
        params = {'H': 200, 'B': 100, 'tw': 10, 'tf': 15}
        with patch('sys.stdout', new=io.StringIO()):
            self.assertTrue(Validator.validate_beam(params)[0])

    def test_validate_beam_invalid_H(self):
        params = {'H': 0, 'B': 100, 'tw': 10, 'tf': 15} # H too small (min is 1)
        with patch('sys.stdout', new=io.StringIO()):
            self.assertFalse(Validator.validate_beam(params)[0])

    def test_validate_beam_invalid_B(self):
        params = {'H': 200, 'B': 0, 'tw': 10, 'tf': 15} # B too small
        with patch('sys.stdout', new=io.StringIO()):
            self.assertFalse(Validator.validate_beam(params)[0])

    def test_validate_beam_invalid_tw(self):
        params = {'H': 200, 'B': 100, 'tw': 0, 'tf': 15} # tw too small
        with patch('sys.stdout', new=io.StringIO()):
            self.assertFalse(Validator.validate_beam(params)[0])

    def test_validate_beam_invalid_tf(self):
        params = {'H': 200, 'B': 100, 'tw': 10, 'tf': 0} # tf too small
        with patch('sys.stdout', new=io.StringIO()):
            self.assertFalse(Validator.validate_beam(params)[0])

    def test_validate_beam_H_B_ratio_warning(self):
        params = {'H': 1500, 'B': 100, 'tw': 10, 'tf': 15} # H/B = 15 > 10
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            # This should still return True as it's a warning, not an error
            self.assertTrue(Validator.validate_beam(params)[0])
            self.assertIn("Warning: H/B ratio exceeds 10", fake_out.getvalue())

    def test_validate_column_valid(self):
        params = {'width': 100, 'height': 500}
        with patch('sys.stdout', new=io.StringIO()):
            self.assertTrue(Validator.validate_column(params)[0])

    def test_validate_column_invalid_width(self):
        params = {'width': 0, 'height': 500} # width too small
        with patch('sys.stdout', new=io.StringIO()):
            self.assertFalse(Validator.validate_column(params)[0])

    def test_validate_column_invalid_height(self):
        params = {'width': 100, 'height': 0} # height too small
        with patch('sys.stdout', new=io.StringIO()):
            self.assertFalse(Validator.validate_column(params)[0])

if __name__ == '__main__':
    unittest.main()
