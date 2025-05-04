from enum import Enum


SUITS = ["♠", "♥", "♣", "♦"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

NUMBER_OF_DECKS = 4
MIN_BET = 5

class Actions(Enum):
    PLAY = "play"
    ACCOUNT = "account"
    EXIT = "exit"

class GameActions(Enum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE_DOWN = "double"
    SPLIT = "split"
    SURRENDER = "surrender"

class AccountActions(Enum):
    ADD_FUNDS = "add funds"
    REMOVE_ACCOUNT = "delete account"
    CHANGE_PASSWORD = "change password"
    CHANGE_USERNAME = "change username"
    VIEW_BALANCE = "view balance"
    BACK = "back"