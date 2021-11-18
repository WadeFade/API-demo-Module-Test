import unittest

from utils import utils


class TestCapitalize(unittest.TestCase):
    def test_method_capitalize(self):
        self.assertEqual(utils.capitalize('abcdefg'), 'Abcdefg')
