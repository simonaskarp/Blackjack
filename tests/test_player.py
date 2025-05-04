import unittest
from dealer import Dealer
from user import User
from cards import Card

class TestDealer(unittest.TestCase):
    def setUp(self):
        self.dealer = Dealer()

    def test_dealer_decision(self):
        """Test dealer's decision making"""
        # Should hit on 16
        self.dealer.game_cards = [Card("8", "♠"), Card("8", "♥")]
        self.assertTrue(self.dealer.make_decision())
        
        # Should stand on 17
        self.dealer.game_cards = [Card("10", "♠"), Card("7", "♥")]
        self.assertFalse(self.dealer.make_decision())

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("test_user", "password", 1000)

    def test_split_eligibility(self):
        """Test if user can split pairs"""
        self.user.game_cards = [Card("10", "♠"), Card("10", "♥")]
        self.user.bet_amount = 100
        self.assertTrue(self.user.can_split())

        self.user.game_cards = [Card("10", "♠"), Card("9", "♥")]
        self.assertFalse(self.user.can_split())