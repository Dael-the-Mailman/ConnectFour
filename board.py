import numpy as np
from copy import deepcopy

class Board:
    def __init__(self, board=None):
        self.width = 7
        self.height = 6
        self.board = np.asarray([" "] * self.width * self.height).reshape(6,7)
        self.player1 = True

        if board is not None:
            self.__dict__  = deepcopy(board.__dict__)

    def __str__(self):
        out = "".join(["-"]*29)
        for row in self.board:
            out += "\n| " + " | ".join(row) + " |\n" + "".join(["-"]*29)
        out += "\n  " + "   ".join(str(i) for i in range(self.width))
        return out

    def place_piece(self, column):
        if self.is_full_column(column):
            print("Invalid Move")
            return
        for i in range(self.height - 1, -1, -1):
                if(self.board[i][column] == " "):
                    self.board[i][column] = 'X' if self.player1 else "O"
                    break

    def check_win(self, column):
        for i in range(self.height):
            if self.board[i][column] != " ":
                row = i
                break
        
        # Check all four directions using a sliding window

        # Horizontal
        for i in range(4):
            sublist = self.board[row][column - 3 + i : column + i + 1]
            if len(sublist) == 4:
                res = all(element == sublist[0] for element in sublist)
                if res:
                    return True
                
        # Vertical
        for i in range(4):
            sublist = np.transpose(self.board)[column][row  - 3 + i : row + i + 1]
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
                    sublist.append(self.board[newRow][newColumn])
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
                    sublist.append(self.board[newRow][newColumn])
                if len(sublist) == 4:
                    res = all(element == sublist[0] for element in sublist)
                    if res:
                        return True
            except:
                pass
        
        return False

    def is_full_board(self):
        for i in range(self.width):
            if self.board[0][i] == " ":
                return False
        return True

    def is_full_column(self, column):
        return self.board[0][column] != " "

    def play(self):
        print(self)
        while True:
            # Process User Input
            if self.player1:
                print("X's turn")
            else:
                print("O's turn")
            user_input = input("Select from columns 0-6 or type exit: ")
            if(user_input == 'exit'):
                break
            if(user_input == ''):
                continue
            user_input = int(user_input)
            if(user_input > 6 or user_input < 0):
                print("Invalid Move")
                continue
            
            # If User input is valid then place the piece on the board
            self.place_piece(user_input)
            print(self) # Print board once piece placed
            
            # Check if the user won the game
            if(self.check_win(user_input)):
                if(self.player1):
                    print("X WINS!!!")
                    break
                else:
                    print("O WINS!!!")
                    break
            
            # If the user hasn't won check if the board is drawn
            if(self.is_full_board()):
                print("DRAW")
                break
            
            # Switch players if everything else is false
            self.player1 = not self.player1
    
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
        
    def get_next_state(self, action):
        board = Board(self)
        board.player1 = not board.player1
        board.place_piece(action)
    
if __name__ == "__main__":
    board = Board()
    print("""
 ██████  ██████  ███    ██ ███    ██ ███████  ██████ ████████     ███████  ██████  ██    ██ ██████  
██      ██    ██ ████   ██ ████   ██ ██      ██         ██        ██      ██    ██ ██    ██ ██   ██ 
██      ██    ██ ██ ██  ██ ██ ██  ██ █████   ██         ██        █████   ██    ██ ██    ██ ██████  
██      ██    ██ ██  ██ ██ ██  ██ ██ ██      ██         ██        ██      ██    ██ ██    ██ ██   ██ 
 ██████  ██████  ██   ████ ██   ████ ███████  ██████    ██        ██       ██████   ██████  ██   ██ 
                                                                                                                                                                                          
    """)
    board.play()
