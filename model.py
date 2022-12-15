import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

class MockModel():
    def __init__(self, game):
        self.game = game

    def predict(self, board):
        # Return probabilities and value the position as 0
        probs = self.game.get_valid_moves(board)
        probs /= probs.sum()
        return probs, 0

class ConnectFourModel(nn.Module):
    def __init__(self, game, device):
        super(ConnectFourModel, self).__init__()
        self.game = game
        self.device = device

        self.to(device)

    def forward(self, x):
        pass

    def predict(self, board):
        pass