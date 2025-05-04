import decks
import user
import dealer
import time
import os
from constants import Actions as A, GameActions as GA, MIN_BET


class GameController:
    def __init__(self):
        self.deck = decks.Deck()
        self.deck.shuffle_cards()
        # self.deck.debug_split_hands_deck()  # For debugging split hands (3 splits, 4 hands)
        self.dealer = dealer.Dealer()
        self.user = None
        self.play = False  # Add play state variable
        self.hand_split = False 
    
    def start_game(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to the Blackjack Game!")
        self.login_user()
        self.play = True  # Set play to True after successful login
    
    def handle_action(self):
        """Handle main menu actions"""
        action = self.user.make_decision(playing=False)
        if action == A.PLAY.value:
            self.play_round()
        elif action == A.EXIT.value:
            self.save_and_exit()
            self.play = False  # Set play to False to exit game

    def login_user(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        try:
            self.user = user.User.load_player_data(username, password)
            print(f"Welcome back, {self.user.username}!")
            print(f"Your current balance is: €{self.user.balance:.2f}")
        except ValueError as e:
            print(e)
            self.register_user(username, password)
    
    def register_user(self, username, password):
        initial_balance = float(input("Enter your initial balance: €"))
        self.user = user.User(username, password, initial_balance)
        self.user.save_player_data()
        print(f"User {self.user.username} registered successfully!")

    def place_bet(self):
        while True:
            try:
                print(f"\nYour balance: €{self.user.balance:.2f}")
                print(f"Minimum bet: €{MIN_BET:.2f}")
                bet = float(input("Enter your bet amount: €"))
                self.user.bet_amount = bet
                self.user.balance -= bet
                break
            except ValueError as e:
                print(e)

    def play_round(self):
        """Handles the logic for playing a round of Blackjack."""
        os.system('cls' if os.name == 'nt' else 'clear')
        # Check if deck needs shuffling
        if self.dealer.should_shuffle(len(self.deck.cards)):
            print("\nDealer is shuffling the deck...")
            time.sleep(1.5)
            self.deck = decks.Deck()
            self.deck.shuffle_cards()

        # Prepare for new round
        self.user.clear_cards()
        self.user.clear_splits()
        self.dealer.clear_cards()
        self.place_bet()

        # Initial deal
        for _ in range(2):
            self.user.draw_card(self.deck.draw_card())
            self.dealer.draw_card(self.deck.draw_card())

        # Show initial hands
        self.show_game_state(hide_dealer=True)
        
        # Player's turn
        self.player_turn()

        if self.user.split_hands:
            self.play_split_hands()
        else:
            # Dealer's turn if player hasn't busted
            if self.user.score <= 21:
                os.system('pause')
                self.dealer_turn()
                self.show_game_state(hide_dealer=False)
                self.determine_winner()
            else:
                print("\nBust! You lose!")

            os.system('pause')

    def play_split_hands(self):
        """Handles the logic for playing split hands."""
        nobust_split_hands = []
        nobust_split_bets = []
        self.hand_split = True
        
        while self.user.split_hands:
            hand = self.user.split_hands.pop(0)
            bet = self.user.split_bets.pop(0)
            self.user.game_cards = hand
            self.user.bet_amount = bet
            
            self.show_game_state(hide_dealer=True)
            self.player_turn()
            
            if self.user.score == 0:
                continue # skip because player split his hand
            elif self.user.score <= 21:
                nobust_split_hands.append(hand)
                nobust_split_bets.append(bet)
                os.system('pause')
            else:
                print("\nBust! You lost this hand!")
                os.system('pause')

        if nobust_split_hands:
            self.dealer_turn()
            for i, hand in enumerate(nobust_split_hands):
                self.user.game_cards = hand
                self.user.bet_amount = nobust_split_bets[i]
                self.show_game_state(hide_dealer=False)
                self.determine_winner()
                os.system('pause')

    def show_game_state(self, hide_dealer=True):
        """Displays the current game state."""
        os.system('cls' if os.name == 'nt' else 'clear')
        if not hide_dealer: 
            print("\n»»»»» DEALER'S TURN «««««")
        else: 
            print(f"\n»»»»» {self.user.username.upper()}'s TURN «««««")
        print("\n" + "═"*40)

        print("Dealer's hand:")
        self.dealer.card_showing = not hide_dealer
        self.dealer.display_cards(hide_second=hide_dealer)
        print(f"Score: {self.dealer.get_visible_score()}")
    
        # if hide_dealer and len(visible_cards) > 0:
        #     print(f"[{visible_cards[0].code}, **]")
        # else:
        #     print([card.code for card in visible_cards])
        # print(f"Score: {self.dealer.get_visible_score()}")

        print("\nYour hand:")
        self.user.display_cards(hide_second=False)
        print(f"Score: {self.user.score}")
        print(f"Current bet: €{self.user.bet_amount:.2f}")
        print("═"*40)

        if self.hand_split:
            print(f"\nSplit hand with bet: €{self.user.bet_amount:.2f}")

    def player_turn(self):
        """Handles the logic for the player's turn."""
        while self.user.score < 21:
            decision = self.user.make_decision(playing=True)
            if decision == GA.HIT.value:
                self.handle_hit()
            elif decision == GA.DOUBLE_DOWN.value:
                self.handle_double()
                break
            elif decision == GA.SPLIT.value:
                self.handle_split()
                break
            elif decision == GA.STAND.value:
                break
    
    def handle_hit(self):
        """Handles the logic for hitting."""
        self.user.draw_card(self.deck.draw_card())
        self.show_game_state(hide_dealer=True)

    def handle_double(self):
        """Handles the logic for doubling down."""
        self.user.balance -= self.user.bet_amount
        self.user.bet_amount *= 2
        self.user.draw_card(self.deck.draw_card())
        self.show_game_state(hide_dealer=True)

    def handle_split(self):
        """Handles the logic for splitting the player's hand."""
        split_card = self.user.split_hand()

        hand1 = self.user.game_cards + [self.deck.draw_card()]
        hand2 = [split_card] + [self.deck.draw_card()]

        self.user.clear_cards()

        self.user.split_hands.extend([hand1, hand2])
        self.user.split_bets.extend([self.user.bet_amount, self.user.bet_amount])

        self.user.balance -= self.user.bet_amount

    def dealer_turn(self):
        """Handles the logic for the dealer's turn."""
        self.show_game_state(hide_dealer=False)
        time.sleep(1)
        while self.dealer.make_decision():
            self.dealer.draw_card(self.deck.draw_card())
            self.show_game_state(hide_dealer=False)
            time.sleep(1.5)

    def determine_winner(self):
        """Handles the logic for determining the winner of the round."""
        dealer_score = self.dealer.score
        player_score = self.user.score
        
        if dealer_score > 21:
            print(f"\nDealer busts! You win €{self.user.bet_amount}!")
            self.user.balance += self.user.bet_amount * 2
        elif dealer_score > player_score:
            print("\nDealer wins!")
        elif dealer_score < player_score:
            print(f"\nYou win €{self.user.bet_amount}!")
            self.user.balance += self.user.bet_amount * 2
        else:
            print("\nPush!")
            self.user.balance += self.user.bet_amount

    def save_and_exit(self):
        self.user.save_player_data()
        print(f"\nThanks for playing! Your final balance is: ${self.user.balance:.2f}")
        print("Your progress has been saved.")