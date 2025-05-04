class Card():
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
        self.code = rank + suit

    def get_card_info(self):
        info = {
            "code": self.code,
            "suit": self.suit,
            "rank": self.rank,
            "value": self.get_card_value()
        }
        return info

    def get_card_value(self):
        if self.rank in ["J", "Q", "K"]:
            return [10]
        elif self.rank == "A":
            return [1, 11]
        else:
            return [int(self.rank)]
        
    def get_card_ascii(self):
        """Generate ASCII art representation of a card"""
        top =    f"┌─────────┐"
        middle = f"│{self.rank:<2}       │"
        suit_line = f"│    {self.suit}    │"
        middle2 = f"│       {self.rank:>2}│"
        bottom = f"└─────────┘"
        
        return [top, middle, suit_line, middle2, bottom]