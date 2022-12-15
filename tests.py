import numpy as np
import unittest
from board import Connect4Game, PLAYER_X, PLAYER_O
from mcts_no_priors import MCTS, Node

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

    def test_is_win(self):
        init = self.game.get_init_board()
        self.assertFalse(self.game.is_win(init))

        horizontal = np.zeros((6,7))
        horizontal[0][0] = 1
        horizontal[0][1] = 1
        horizontal[0][2] = 1
        horizontal[0][3] = 1

        self.assertTrue(self.game.is_win(horizontal))

        horizontal = np.zeros((6,7))
        horizontal[0][0] = 1
        horizontal[0][1] = -1
        horizontal[0][2] = 1
        horizontal[0][3] = 1
        self.assertFalse(self.game.is_win(horizontal))

        b1 = np.array(
        [[0,  0,  0,  0,  0,  0,  0],
         [0,  0,  -1,  0,  -1,  0,  0],
         [0,  0,  1,  1,  1,  0,  0],
         [0,  1,  -1,  1,  -1,  1,  0],
         [0,  -1,  1,  -1,  1,  -1,  0],
         [1,  -1,  1,  -1,  1,  -1,  1]])
        self.assertFalse(self.game.is_win(b1))

        b2 = np.array(
        [[0,  0,  0,  0,  0,  0,  0],
         [0,  0,  -1, 0,  -1,  0,  0],
         [0,  0,  1,  -1,  1,  0,  0],
         [0,  1,  -1,  1,  -1,  1,  0],
         [0,  -1,  1,  -1,  1,  -1,  0],
         [1,  -1,  1,  -1,  1,  -1,  1]])
        self.assertTrue(self.game.is_win(b2))


    def test_get_valid_moves(self):
        b = self.game.get_init_board()
        valid_moves = self.game.get_valid_moves(b)
        test_moves = np.array([1] * 7)
        self.assertTrue((valid_moves == test_moves).all())

        for i in range(self.game.height):
            b[i][0] = 1
        valid_moves = self.game.get_valid_moves(b)
        self.assertFalse((valid_moves == test_moves).all())
        test_moves[0] = 0
        self.assertTrue((valid_moves == test_moves).all())

        for i in range(self.game.height):
            b[i][5] = 1
        valid_moves = self.game.get_valid_moves(b)
        self.assertFalse((valid_moves == test_moves).all())
        test_moves[5] = 0
        self.assertTrue((valid_moves == test_moves).all())

    def test_get_next_state(self):
        b = self.game.get_init_board()
        player = PLAYER_O

        b, player = self.game.get_next_state(b, player, 5)
        ref_b = np.zeros((6,7))
        ref_b[5][5] = -1
        self.assertEqual(player, 1)
        self.assertTrue((ref_b == b).all())

        b, player = self.game.get_next_state(b, player, 5)
        ref_b[4][5] = 1
        self.assertEqual(player, -1)
        self.assertTrue((ref_b == b).all())

        b, player = self.game.get_next_state(b, player, 0)
        ref_b[5][0] = -1
        self.assertEqual(player, 1)
        self.assertTrue((ref_b == b).all())

    def test_get_canonical_board(self):
        b = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0],
                [0, 0, -1, 1, 1, -1, 1],
                [0, -1, -1, -1, -1, 1, 1]
            ]
        )
        test_b = self.game.get_canonical_board(b, PLAYER_X)
        self.assertTrue((test_b == b).all())
        self.assertFalse((test_b == -b).all())

        test_b = self.game.get_canonical_board(b, PLAYER_O)
        self.assertTrue((test_b == -b).all())
        self.assertFalse((test_b == b).all())

    def test_get_reward_for_player(self):
        b = self.game.get_init_board()
        b[5][3] = 1
        b[5][5] = -1
        self.assertIsNone(self.game.get_reward(b, PLAYER_X, 3))
        self.assertIsNone(self.game.get_reward(b, PLAYER_O, 5))

        b = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0],
                [0, 0, -1, 1, 1, -1, 1],
                [0, -1, -1, -1, -1, 1, 1]
            ]
        )
        self.assertEqual(self.game.get_reward(b, PLAYER_O, 1), 1)
        self.assertEqual(self.game.get_reward(b, PLAYER_X, 1), -1)

        b = self.game.get_canonical_board(b, PLAYER_O)
        self.assertEqual(self.game.get_reward(b, PLAYER_O, 1), -1)
        self.assertEqual(self.game.get_reward(b, PLAYER_X, 1), 1)

class TestMCTSNoPriors(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMCTSNoPriors, self).__init__(*args, **kwargs)
        self.game = Connect4Game()
        self.mcts = MCTS(self.game)

    def test_init(self):
        b = self.game.get_init_board()
        node = Node(b, self.game)

        self.assertTrue((b == node.board).all())
        self.assertIsNone(node.parent)
        self.assertFalse(node.is_terminal)
        self.assertFalse(node.is_fully_expanded)
        self.assertEqual(node.visits, 0)
        self.assertEqual(node.score, 0)
        self.assertEqual(node.children, {})