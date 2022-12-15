import numpy as np

class Node:
    def __init__(self, board, game, parent=None):
        self.board = board
        self.game = game
        
        if self.game.is_win(board) or self.game.is_full_board(board):
            self.is_terminal = True
        else:
            self.is_terminal = False
        
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.visits = 0 
        self.score = 0
        self.children = {}

class MCTS:
    def __init__(self, game):
        self.game = game

    def search(self, initial_state):
        pass

    def select(self, node):
        pass

    def expand(self, node):
        pass
    
    def rollout(self, board):
        pass

    def backpropagate(self, node, score):
        pass

    def get_best_move(self, node, exploration_constant):
        pass

