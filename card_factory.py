from cards import Card
from constants import SUITS, RANKS


class CardFactory:   
    @staticmethod
    def create_standard_card(rank: str, suit: str) -> Card:
        """Create a standard playing card"""
        return Card(rank, suit)

    @staticmethod
    def create_debug_cards() -> list:
        """Create cards for debugging split hands"""
        return [
            Card("10", "S"),
            Card("5", "S"),
            Card("10", "S"),
            Card("9", "S"),
            Card("10", "S"),
            Card("10", "S")
        ]
    
    @staticmethod
    def create_deck(num_of_decks: int = 1) -> list:
        """Create a full deck of cards"""
        cards = []
        for _ in range(num_of_decks):
            for suit in SUITS:
                for rank in RANKS:
                    cards.append(CardFactory.create_standard_card(rank, suit))
        return cards