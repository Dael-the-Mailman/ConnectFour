import numpy as np
import unittest
from board import Connect4Game

class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameTest, self).__init__(*args, **kwargs)
        self.game = Connect4Game()

    def test_board_dimensionality(self):
        b = self.game.get_init_board()
        self.assertEqual(b.shape, (self.game.height, self.game.width))