import unittest

from mahjong.components import Suit
from mahjong.utils import get_values, get_name, roundup


class TestGetValue(unittest.TestCase):

    def test_get_values(self):
        suit_value = ['JIHAI', 'MANZU', 'SOUZU', 'PINZU']
        self.assertEqual(get_values(Suit), suit_value)


class TestGetName(unittest.TestCase):

    def test_get_name(self):
        self.assertEqual(get_name(Suit, 0), 'JIHAI')


class TestRoundup(unittest.TestCase):

    def test_roundup(self):
        self.assertEqual(roundup(1), 100)



