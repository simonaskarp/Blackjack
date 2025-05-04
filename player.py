from abc import ABC, abstractmethod
from cards import Card


class Player(ABC):
    def __init__(self):
        self._score = 0
        self._game_cards = []

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, new_score):
        self._score = new_score
    
    @property
    def game_cards(self):
        return self._game_cards
    
    @game_cards.setter
    def game_cards(self, new_game_cards):
        self._game_cards = new_game_cards
        self.calculate_score()
    
    def draw_card(self, card):
        """Add a card to player's hand and update score"""
        self._game_cards.append(card)
        self.calculate_score()
    
    def clear_cards(self):
        """Clear player's hand"""
        self._game_cards = []
        self._score = 0
    
    def calculate_score(self):
        """Calculate the total score of cards in hand"""
        self._score = 0
        total_aces = 0
        non_ace_sum = 0

        for card in self._game_cards:
            card_values = card.get_card_value()
            
            if card.rank == 'A':
                total_aces += 1
            else:
                non_ace_sum += card_values[0]

        # Handle aces optimally
        self._score = non_ace_sum
        for _ in range(total_aces):
            if self._score + 11 <= 21:
                self._score += 11
            else:
                self._score += 1

    def display_cards(self, hide_second=False):
        """Display multiple cards side by side"""
        if not self.game_cards:
            return
        
        # Get ASCII representation for each card
        card_list = []
        for i, card in enumerate(self.game_cards):
            if i == 1 and hide_second:
                hidden_card = Card("?", "?")
                card_list.append(hidden_card.get_card_ascii())
            else:
                card_list.append(card.get_card_ascii())
        
        # Combine cards side by side
        for i in range(5):  # 5 lines per card
            line = ""
            for card_ascii in card_list:
                line += card_ascii[i] + " "
            print(line)
    
    @abstractmethod
    def make_decision(self):
        """Player decides to hit or stand"""
        pass