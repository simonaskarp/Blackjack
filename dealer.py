from player import Player


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.__card_showing = False
        self.__shuffle_threshold = 52  # Reshuffle when this many cards remain
    
    @property
    def card_showing(self):
        return self.__card_showing
    
    @card_showing.setter
    def card_showing(self, value):
        self.__card_showing = value
    
    def make_decision(self):
        """Dealer's automated decision based on standard rules"""
        return self.score < 17  # Dealer must hit on 16 and below
    
    def should_shuffle(self, remaining_cards):
        """Decides if deck should be shuffled based on remaining cards"""
        return remaining_cards <= self.__shuffle_threshold
    
    def get_visible_score(self):
        """Returns only the score of visible cards when hiding second card"""
        if not self.__card_showing and len(self._game_cards) > 0:
            return self._game_cards[0].get_card_value()[0]
        return self.score
    
    def get_visible_cards(self):
        """Returns list of visible cards (hides second card if not showing)"""
        if not self.__card_showing and len(self._game_cards) > 1:
            return [self._game_cards[0]]
        return self._game_cards