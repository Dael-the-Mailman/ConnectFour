import numpy as np
from copy import deepcopy

PLAYER_X = 1
PLAYER_O = -1

class Connect4Game:
    def __init__(self):
        self.width = 7
        self.height = 6
        # self.board = np.asarray([" "] * self.width * self.height).reshape(6,7)
        # self.player1 = True

        # if board is not None:
        #     self.__dict__  = deepcopy(board.__dict__)

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

    def check_win(self, board, column):
        for i in range(self.height):
            if board[i][column] != 0:
                row = i
                break
        
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
    
    def get_reward(self, column):
        if self.is_win(column):
            return 1 if self.player1 else -1
        if not self.is_full_board():
            return None
        return 0
    
    def get_valid_moves(self):
        valid_moves = [0] * self.width
        for col in range(self.width):
            if not self.is_full_column(col):
                valid_moves[col] = 1
        return valid_moves

    def get_canonical_board(self):
        board = np.zeros(self.board.shape)
        for row in range(self.height):
            for col in range(self.width):
                if self.player1:
                    multiplier = 1 if self.board[row][col] == "X" else -1
                    board[row][col] = 1 if self.board[row][col] != " " else 0
                    board[row][col] *= multiplier
                else:
                    multiplier = 1 if self.board[row][col] == "O" else -1
                    board[row][col] = 1 if self.board[row][col] != " " else 0
                    board[row][col] *= multiplier
        return board
        
    def get_next_state(self, board, player, action):
        b = np.copy(board)
        b = self.place_piece(board, player, action)