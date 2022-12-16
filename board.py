import numpy as np
from copy import deepcopy

PLAYER_X = 1
PLAYER_O = -1

class Connect4Game:
    def __init__(self):
        self.width = 7
        self.height = 6

    def print_board(self, board):
        out = "".join(["-"]*29)
        for row in range(self.height):
            out += "\n" 
            for col in range(self.width):
                out += "| "
                state = board[row][col]
                if state == 0:
                    out += " "
                if state == 1:
                    out += "X"
                if state == -1:
                    out += "O"
                out += " "
            out += "|\n" + "".join(["-"]*29)
        out += "\n  " + "   ".join(str(i) for i in range(self.width))
        print(out)
    
    def get_init_board(self):
        board = np.zeros((self.height, self.width))
        return board

    def get_board_size(self):
        return (self.height, self.width)

    def get_action_size(self):
        return self.width

    def place_piece(self, board, player, column):
        if self.is_full_column(board, column):
            print("Invalid Move")
            return
        for i in range(self.height - 1, -1, -1):
                if(board[i][column] == 0):
                    board[i][column] = player
                    break
        return board

    def is_win(self, board):
        for i in range(self.get_action_size()):
            if self.check_win(board, i):
                for j in range(self.height):
                    if board[j][i] != 0:
                        return True, board[j][i]
        return False, None

    def check_win(self, board, column):
        row = None
        for i in range(self.height):
            if board[i][column] != 0:
                row = i
                break
        
        if row == None:
            return False

        # Check all four directions using a sliding window

        # Horizontal
        for i in range(4):
            sublist = board[row][column - 3 + i : column + i + 1]
            if len(sublist) == 4:
                res = all(element == sublist[0] for element in sublist)
                if res:
                    return True
                
        # Vertical
        for i in range(4):
            sublist = np.transpose(board)[column][row  - 3 + i : row + i + 1]
            if len(sublist) == 4:
                res = all(element == sublist[0] for element in sublist)
                if res:
                    return True

        # Positive Diagonal
        for i in range(4):
            try:
                sublist = []
                for j in range(4):
                    newRow = row + i - j
                    newColumn = column - i + j
                    if newRow < 0 or newColumn < 0:
                        continue
                    sublist.append(board[newRow][newColumn])
                if len(sublist) == 4:
                    res = all(element == sublist[0] for element in sublist)
                    if res:
                        return True
            except:
                pass

        # Negative Diagonal
        for i in range(4):
            try:
                sublist = []
                for j in range(4):
                    newRow = row + i - j
                    newColumn = column + i - j
                    if newRow < 0 or newColumn < 0:
                        continue
                    sublist.append(board[newRow][newColumn])
                if len(sublist) == 4:
                    res = all(element == sublist[0] for element in sublist)
                    if res:
                        return True
            except:
                pass
        
        return False

    def is_full_board(self, board):
        for i in range(self.width):
            if board[0][i] == 0:
                return False
        return True

    def is_full_column(self, board, column):
        return board[0][column] != 0
    
    def get_reward(self, board, player):
        # return None if not ended, 1 if player 1 wins, -1 if player 1 lost
        win, play = self.is_win(board)
        if win:
            if play == player:
                return 1
            else:
                return -1
        if not self.is_full_board(board):
            return None
        return 0
    
    def get_valid_moves(self, board):
        valid_moves = np.zeros(self.get_action_size())
        for col in range(self.width):
            if not self.is_full_column(board, col):
                valid_moves[col] = 1
        return valid_moves

    def get_canonical_board(self, board, player):
        return board * player
        
    def get_next_state(self, board, player, action):
        b = np.copy(board)
        b = self.place_piece(board, player, action)

        return (b, -player)