import unittest
import os
from pathlib import Path

from .utils import check_code


class CheckCodeTestCase(unittest.TestCase):

    def setUp(self):
        with open('valid_test_code.py', 'w+') as valid_file:
            valid_file.write("def foo():\n    pass\n")
        self.valid_code_path = Path.cwd().joinpath(valid_file.name)

        with open('invalid_test_code.py', 'w+') as invalid_file:
            invalid_file.write("foo(")
        self.invalid_code_path = Path.cwd().joinpath(invalid_file.name)

    def test_valid_code(self):
        errors, valid = check_code(
            str(self.valid_code_path.absolute()))
        self.assertTrue(valid)
        self.assertEqual(errors, [])

    def test_invalid_code(self):
        errors, valid = check_code(
            str(self.invalid_code_path.absolute()))
        self.assertFalse(valid)
        self.assertEqual(len(errors), 2)

    def tearDown(self):
        self.valid_code_path.unlink()
        self.invalid_code_path.unlink()
