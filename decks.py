import random
from constants import NUMBER_OF_DECKS
from card_factory import CardFactory


class Deck():
    def __init__(self, num_of_decks=NUMBER_OF_DECKS):
        self.num_of_decks = num_of_decks
        self.cards = []
        self.create_deck()
    
    def create_deck(self):
        self.cards = CardFactory.create_deck(self.num_of_decks)

    def get_cards_info(self):
        card_info = []
        for card in self.cards:
            card_info.append(card.get_card_info())
        return card_info

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def draw_card(self):
        card = self.cards[0]
        self.cards.pop(0)
        return card
    
    def debug_split_hands_deck(self):
        """Debugging function to make a deck to draw a split hand"""
        splitting_cards = CardFactory.create_debug_cards()
        self.cards = splitting_cards + self.cards