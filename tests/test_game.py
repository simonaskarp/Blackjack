import unittest
from dealer import Dealer
from user import User
from game_controller import GameController
from cards import Card

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game = GameController()
        self.game.user = self.create_test_user()
        self.game.dealer = self.create_test_dealer()

    def create_test_user(self):
        user = User("test", "test", 1000)
        return user

    def create_test_dealer(self):
        dealer = Dealer()
        return dealer

    def test_blackjack_win(self):
        """Test blackjack winning condition"""
        self.game.user.game_cards = [Card("A", "♠"), Card("K", "♥")]
        self.game.dealer.game_cards = [Card("10", "♠"), Card("9", "♥")]
        self.game.user.bet_amount = 100
        
        initial_balance = self.game.user.balance
        self.game.determine_winner()
        self.assertEqual(self.game.user.balance, initial_balance + 200)

    def test_push_condition(self):
        """Test push condition"""
        self.game.user.game_cards = [Card("10", "♠"), Card("10", "♥")]
        self.game.dealer.game_cards = [Card("K", "♠"), Card("10", "♥")]
        self.game.user.bet_amount = 100
        
        initial_balance = self.game.user.balance
        self.game.determine_winner()
        self.assertEqual(self.game.user.balance, initial_balance + 100)