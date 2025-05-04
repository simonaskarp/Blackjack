import unittest
from cards import Card

class TestCard(unittest.TestCase):
    def setUp(self):
        self.ace = Card("A", "♠")
        self.king = Card("K", "♥")
        self.ten = Card("10", "♣")

    def test_card_values(self):
        """Test card value calculations"""
        self.assertEqual(self.ace.get_card_value(), [1, 11])
        self.assertEqual(self.king.get_card_value(), [10])
        self.assertEqual(self.ten.get_card_value(), [10])

    def test_card_info(self):
        """Test card information structure"""
        info = self.ace.get_card_info()
        self.assertEqual(info["code"], "A♠")
        self.assertEqual(info["value"], [1, 11])