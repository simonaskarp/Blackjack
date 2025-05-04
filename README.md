# Blackjack

## Introduction

### What is your application?
This is a console-based Blackjack game implemented in Python using Object-Oriented Programming principles. The game features:
- Full blackjack gameplay including hit, stand, double down, and split actions
- Player account system with persistent data storage
- Multiple deck support with automatic shuffling
- ASCII card visualization
- Balance management system
- Dealer AI following standard casino rules

### How to run the program?
1. Ensure you have Python 3.x installed on your system
2. Clone the repository:
```bash
git clone https://github.com/simonaskarp/Blackjack.git
cd blackjack
```
3. Run the main program:
```bash
python main.py
```

### How to use the program?
1. **First Launch**:
   - Enter a username and password
   - Set your initial balance
   
2. **Main Menu**:
   - `play` - Start a new game round
   - `account` - Access account management
   - `exit` - Save and quit the game

3. **During Game**:
   - Enter bet amount (minimum €5)
   - Choose from available actions:
     - `hit` - Draw another card
     - `stand` - Keep current hand
     - `double` - Double your bet and receive one final card
     - `split` - Split paired cards into two hands (requires matching bet)

4. **Account Management**:
   - Add funds
   - View balance
   - Change username/password
   - Delete account
  
## Implementation Analysis

### Object-Oriented Programming Pillars

1. **Encapsulation**
   - Bundling data and methods that operate on that data within a single unit (class)
   - Restricts direct access to object components, hiding internal details
   - Implementation using private attributes (`__`) and getters/setters (properties)
   - Private attributes in `User` class using double underscores (e.g., `__username`, `__password`)
   - Property decorators for controlled access to attributes
   - Example from `user.py`:
   ```python
   @property
   def balance(self):
       return self.__balance
   
   @balance.setter
   def balance(self, amount):
       self.__balance = amount
   ```

2. **Inheritance**
   - Mechanism that allows a class to inherit properties and methods from another class
   - Promotes code reuse and establishes relationships between classes
   - Implementation using base/parent class to share common functionality
   - `Player` serves as base class for both `User` and `Dealer`
   - Common functionality like card handling shared through inheritance
   - How it is used:
   ```py
   class Player(ABC):
     pass

   class User(Player):
     pass

   class Dealer(Player):
     pass
   ```

3. **Polymorphism**
   - Ability of different classes to be treated as instances of the same class
   - Enables using different class types through the same interface
   - Implementation through method overriding and common interfaces
   - `make_decision()` method implemented differently in `User` and `Dealer`
   - Same method name, different behaviors based on class
   - Usage example:
   ```python
   # Dealer class implementation
   def make_decision(self):
       return self.score < 17

   # User class implementation
   def make_decision(self, playing=False):
        if playing:
            return self.show_play_menu()
        else:
            return self.show_main_menu()
   ```

4. **Abstraction**
   - Hiding complex implementation details and showing only functionality
   - Reduces complexity and isolates impact of changes
   - Abstract base class `Player` with `@abstractmethod`
   - Hides complexity of card handling and score calculation
   - Common interface for both dealer and user
   ```py
   from abc import ABC, abstractmethod

   
   class Player(ABC):

   @abstractmethod
    def make_decision(self):
        """Player decides to hit or stand"""
        pass
   ```

### Design Patterns
- The Factory Method Design Pattern is a creational design pattern that provides an interface for creating objects in a superclass, allowing subclasses to alter the type of objects that will be created. This pattern is particularly useful when the exact types of objects to be created may vary
- **Factory Pattern** implemented in `CardFactory` class
- Creates different types of cards and decks in `Deck` class
- Centralizes object creation logic
```py
from cards import Card
from constants import SUITS, RANKS


class CardFactory:   
    @staticmethod
    def create_standard_card(rank: str, suit: str) -> Card:
        """Create a standard playing card"""
        return Card(rank, suit)

    @staticmethod
    def create_debug_cards() -> list:
        """Create cards for debugging split hands (creates 3 splits, 4 hands)"""
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
```

### Composition/Aggregation
- Composition is a strong "has-a" relationship where child cannot exist without parent
- Aggregation is a weak "has-a" relationship where child can exist independently
- Game has Deck (composition), Deck has Cards (aggregation)
- Example from `game_controller.py`:
```python
import decks
import user
import dealer


class GameController:
  def __init__(self):
      self.deck = decks.Deck()
      self.dealer = dealer.Dealer()
      self.user = None
```

### File Operations
- Loading saved game states, user profiles, or configurations
- Player data persistence through file operations
- Saves and loads user account information
- Example from `User` class in `user.py`:
```python
def save_player_data(self):
    # Saves user data to JSON file

def load_player_data(cls, username, password):
    # Load player data from JSON file
```

### Unit Testing
- Verifies individual components work as expected
- Core functionality covered with unittest framework
- Tests for card creation, scoring, and game logic
- Test files follow naming convention `test_*.py`
- Example of test for cards:
```py
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
```
Checks whether returned card information is correct

## PEP8 Style Guidelines
- **Naming Conventions**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
- **Indentation**: 4 spaces
- **Line Length**: Maximum 79 characters
- **Imports**: At the top of the file, grouped properly

## Results and Summary

### Results
- Successfully implemented a fully functional Blackjack game with standard casino rules and betting system using object-oriented principles.
- Faced challenges with managing multiple split hands and their respective bet amounts, solved by implementing a list-based hand management system.
- Implementing the optimal Ace value calculation (1 or 11) required careful consideration of multiple scenarios to maximize hand value without busting.
- Complex dealer AI decision-making system was simplified by following strict casino rules (hit on 16 or below, stand on 17 or above).
- User data persistence required careful consideration of file handling and error management to prevent data corruption.

### Conclusions

#### Key Achievements
1. Created a robust console-based Blackjack implementation that:
   - Follows casino rules accurately
   - Manages player accounts and balances
   - Provides intuitive ASCII-based card visualization
   - Handles complex game scenarios like splitting and double downs

2. Technical Accomplishments:
   - Clean, maintainable code structure using OOP principles
   - Efficient card management system with multiple deck support
   - Secure user data handling with file persistence
   - Comprehensive error handling for user inputs

#### Future Prospects

1. Additional Blackjack Features:
   - Insurance bets when dealer shows an Ace
   - Multi-seat play (one player controlling multiple hands)
   - Side bets (Perfect Pairs, 21+3)
   - Card counting detection system
   - Statistics tracking and player analytics
   - Tournament mode with leaderboards

2. Online Multiplayer Implementation:
   - Client-server architecture for multiplayer support
   - Real-time gameplay using WebSocket connections
   - Chat system for player interaction
   - Multiplayer tables with varying bet limits
   - Player vs. Player mode without dealer
   - Tournament system with elimination rounds
   - Global ranking system
   - Friend system and private tables
