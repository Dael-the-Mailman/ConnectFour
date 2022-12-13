import numpy as np
from board import Connect4Game, PLAYER_X, PLAYER_O
from mcts import MCTS

print("""
 ██████  ██████  ███    ██ ███    ██ ███████  ██████ ████████     ███████  ██████  ██    ██ ██████  
██      ██    ██ ████   ██ ████   ██ ██      ██         ██        ██      ██    ██ ██    ██ ██   ██ 
██      ██    ██ ██ ██  ██ ██ ██  ██ █████   ██         ██        █████   ██    ██ ██    ██ ██████  
██      ██    ██ ██  ██ ██ ██  ██ ██ ██      ██         ██        ██      ██    ██ ██    ██ ██   ██ 
 ██████  ██████  ██   ████ ██   ████ ███████  ██████    ██        ██       ██████   ██████  ██   ██ 
                                                                                                                                                                                          
    """)
game = Connect4Game()
board = game.get_init_board()
player = PLAYER_X
while True:
    game.print_board(board)
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
    board = game.place_piece(board, player, user_input)
    game.print_board(board) # Print board once piece placed

    if(game.check_win(board, user_input)):
        if(player == PLAYER_X):
            print("X WINS!!!")
            break
        else:
            print("O WINS!!!")
            break
    
    if(game.is_full_board(board)):
        print("DRAW")
        break

    player *= -1