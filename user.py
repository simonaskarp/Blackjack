from player import Player
import json
import os
from constants import Actions as A, GameActions as GA, AccountActions as AA, MIN_BET


class User(Player):
    def __init__(self, username, password, initial_balance=0):
        super().__init__()
        self.__username = ""
        self.__password = ""
        self.__balance = 0
        self.__bet_amount = 0
        self.__split_hands = []
        self.__split_bets = []
        
        self.username = username
        self.password = password
        self.balance = initial_balance

    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, new_username):
        if new_username:
            self.__username = new_username
        else: 
            raise ValueError("Username cannot be NULL")

    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, new_password):
        if new_password:
            self.__password = new_password
        else:
            raise ValueError("Password cannot be NULL")
    
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, amount):
        if amount > 0:
            self.__balance = amount
        else:
            raise ValueError("Balance cannot be negative or zero")
        
    @property
    def bet_amount(self):
        return self.__bet_amount
    
    @bet_amount.setter
    def bet_amount(self, amount):
        if amount < MIN_BET:
            raise ValueError(f"Bet amount must be at least €{MIN_BET:.2f}")
        elif amount > self.__balance:
            raise ValueError("Insufficient funds for this bet!")
        else:
            self.__bet_amount = amount

    @property
    def split_hands(self):
        return self.__split_hands
    
    @property
    def split_bets(self):
        return self.__split_bets
    
    def save_player_data(self):
        """Save player data to a JSON file"""
        player_data = {
            "username": self.__username,
            "password": self.__password,
            "balance": self.__balance
        }
        
        filename = f"players/{self.__username}.json"
        os.makedirs("players", exist_ok=True)
        
        with open(filename, "w") as file:
            json.dump(player_data, file, indent=4)

    @classmethod
    def load_player_data(cls, username, password):
        """Load player data from JSON file"""
        try:
            filename = f"players/{username}.json"
            with open(filename, "r") as file:
                data = json.load(file)
                
            if data["password"] != password:
                raise ValueError("Invalid password")
                
            return cls(
                username=data["username"],
                password=data["password"],
                initial_balance=data["balance"]
            )
        except FileNotFoundError:
            raise ValueError(f"No saved data found for player: {username}")
        
    def can_split(self):
        """Check if hand can be split"""
        return (len(self._game_cards) == 2 and 
                self._game_cards[0].rank == self._game_cards[1].rank and 
                self.balance >= self.bet_amount)

    def split_hand(self):
        """Split hand and return the second card"""
        return self._game_cards.pop()

    def clear_splits(self):
        """Clear split hands and bets"""
        self.__split_hands.clear()
        self.__split_bets.clear()

    def make_decision(self, playing=False):
        if playing:
            return self.show_play_menu()
        else:
            return self.show_main_menu()

    def show_play_menu(self):
        while True:
                actions = f"| {GA.HIT.value} | {GA.STAND.value} |"
                # Only allow double/split on first turn
                if len(self._game_cards) == 2:
                    if self.balance >= self.bet_amount:
                        actions += f" {GA.DOUBLE_DOWN.value} |"
                    if self.can_split():
                        actions += f" {GA.SPLIT.value} |"
                
                print(f"\nAvailable actions: {actions}")
                choice = input("Your action: ").lower()
            
                if choice == GA.HIT.value:
                    return GA.HIT.value
                elif choice == GA.STAND.value:
                    return GA.STAND.value
                elif choice == GA.DOUBLE_DOWN.value and len(self._game_cards) == 2:
                    if self.balance >= self.bet_amount:
                        return GA.DOUBLE_DOWN.value
                    else:
                        print("Insufficient funds to double down!")
                elif choice == GA.SPLIT.value and self.can_split():
                    return GA.SPLIT.value
                else:
                    print(f"Invalid choice! Please enter from available actions.")
    
    def show_main_menu(self):
        while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\nMain Menu:")
                print(f"- {A.PLAY.value}")
                print(f"- {A.ACCOUNT.value}")
                print(f"- {A.EXIT.value}")
                
                choice = input("Your choice: ").lower()
                
                if choice == A.PLAY.value:
                    return A.PLAY.value
                elif choice == A.ACCOUNT.value:
                    self.show_account_menu()
                elif choice == A.EXIT.value:
                    return A.EXIT.value
                else:
                    print("Invalid choice! Please try again.")

    def show_account_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nAccount Menu:")
            for action in AA:
                print(f"- {action.value}")
            
            choice = input("Your choice: ").lower()
            
            if choice == AA.ADD_FUNDS.value:
                self.add_funds()
            elif choice == AA.REMOVE_ACCOUNT.value:
                if self.delete_account():
                    return A.EXIT.value
            elif choice == AA.CHANGE_PASSWORD.value:
                self.change_password()
            elif choice == AA.CHANGE_USERNAME.value:
                self.change_username()
            elif choice == AA.VIEW_BALANCE.value:
                print(f"\nCurrent balance: €{self.balance:.2f}")
                os.system('pause')
            elif choice == AA.BACK.value:
                break
            else:
                print("Invalid choice! Please try again.")
                os.system('pause')

    def add_funds(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                amount = float(input("Enter amount to add: €"))
                if amount <= 0:
                    print("Amount must be positive!")
                else:
                    self.balance += amount
                    print(f"Funds added! New balance: €{self.balance:.2f}")
                    break
            except ValueError:
                print("Invalid input! Please enter a number.")
                os.system('pause')
    
    def delete_account(self):
        """Delete player account and data file"""
        os.system('cls' if os.name == 'nt' else 'clear')
        confirmation = input("Are you sure you want to delete your account? (yes/no): ").lower()
        if confirmation == "yes":
            filename = f"players/{self.__username}.json"
            if os.path.exists(filename):
                os.remove(filename)
                print("Account deleted successfully!")
                os.system('pause')
                return True
            else:
                print("Account not found!")
                os.system('pause')
                return False
        else:
            print("Account deletion cancelled.")
            os.system('pause')
            return False
        
    def change_password(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        old_password = input("Enter current password: ")
        if old_password != self.__password:
            print("Incorrect current password!")
            os.system('pause')
            return
        
        new_password = input("Enter new password: ")
        if new_password:
            self.password = new_password
            self.save_player_data()
            print("Password changed successfully!")
            os.system('pause')
        else:
            print("Password cannot be empty!")
            os.system('pause')

    def change_username(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        new_username = input("Enter new username: ")
        if new_username:
            old_filename = f"players/{self.__username}.json"
            new_filename = f"players/{new_username}.json"
        
            try:
                # Check if new username file already exists
                if os.path.exists(new_filename):
                    print("Username already taken!")
                    os.system('pause')
                    return
                
                # Delete old file first
                if os.path.exists(old_filename):
                    os.remove(old_filename)
                
                # Update username and save
                self.username = new_username
                self.save_player_data()
                print("Username changed successfully!")
                os.system('pause')
            
            except OSError as e:
                print(f"Error changing username: {e}")
                # Revert username if save failed
                self.username = old_filename.split('/')[-1].split('.')[0]
        else:
            print("Username cannot be empty!")
            os.system('pause')