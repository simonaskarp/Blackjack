import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_card import *
from test_player import *
from test_game import *

if __name__ == '__main__':
    unittest.main()