import numpy as np
import unittest
from board import Connect4Game, PLAYER_X, PLAYER_O

class GameTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameTest, self).__init__(*args, **kwargs)
        self.game = Connect4Game()

    def test_board_dimensionality(self):
        b = self.game.get_init_board()
        self.assertEqual(b.shape, (self.game.height, self.game.width))
    
    def test_is_full_column(self):
        b = self.game.get_init_board()
        for row in range(self.game.height):
            b[row][0] = 1
        
        self.assertTrue(self.game.is_full_column(b, 0))
        self.assertFalse(self.game.is_full_column(b, 1))
    
    def test_is_full_board(self):
        b1 = self.game.get_init_board()
        self.assertFalse(self.game.is_full_board(b1))

        b2 = np.random.rand(6,7)
        self.assertTrue(self.game.is_full_board(b2))
        
        b3 = np.array(
        [[0,  0,  0,  1,  0,  0,  0],
         [0,  0,  -1,  1,  -1,  0,  0],
         [0,  0,  1,  1,  1,  0,  0],
         [0,  1,  -1,  1,  -1,  1,  0],
         [0,  -1,  1,  -1,  1,  -1,  0],
         [1,  -1,  1,  -1,  1,  -1,  1]])
        
        self.assertFalse(self.game.is_full_board(b3))

    def test_place_piece(self):
        b = self.game.get_init_board()
        test_b = self.game.place_piece(b, PLAYER_X, 3)
        test_b = self.game.place_piece(test_b, PLAYER_O, 3)
        test_b = self.game.place_piece(test_b, PLAYER_X, 3)
        b[5][3] = 1
        b[4][3] = -1
        b[3][3] = 1
        self.assertTrue((b == test_b).all())
    
    def test_check_win(self):
        horizontal = np.zeros((6,7))
        horizontal[0][0] = 1
        horizontal[0][1] = 1
        horizontal[0][2] = 1
        horizontal[0][3] = 1

        self.assertTrue(self.game.check_win(horizontal, 3))

        horizontal = np.zeros((6,7))
        horizontal[0][0] = 1
        horizontal[0][1] = -1
        horizontal[0][2] = 1
        horizontal[0][3] = 1
        self.assertFalse(self.game.check_win(horizontal, 0))

        b1 = np.array(
        [[0,  0,  0,  0,  0,  0,  0],
         [0,  0,  -1,  0,  -1,  0,  0],
         [0,  0,  1,  1,  1,  0,  0],
         [0,  1,  -1,  1,  -1,  1,  0],
         [0,  -1,  1,  -1,  1,  -1,  0],
         [1,  -1,  1,  -1,  1,  -1,  1]])
        self.assertFalse(self.game.check_win(b1, 3))

        b2 = np.array(
        [[0,  0,  0,  0,  0,  0,  0],
         [0,  0,  -1, 0,  -1,  0,  0],
         [0,  0,  1,  -1,  1,  0,  0],
         [0,  1,  -1,  1,  -1,  1,  0],
         [0,  -1,  1,  -1,  1,  -1,  0],
         [1,  -1,  1,  -1,  1,  -1,  1]])
        self.assertTrue(self.game.check_win(b2, 3))