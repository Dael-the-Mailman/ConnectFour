import numpy as np
from board import Connect4Game, PLAYER_X, PLAYER_O
from mcts_no_priors import MCTS
from model import MockModel

print("""
 ██████  ██████  ███    ██ ███    ██ ███████  ██████ ████████     ███████  ██████  ██    ██ ██████  
██      ██    ██ ████   ██ ████   ██ ██      ██         ██        ██      ██    ██ ██    ██ ██   ██ 
██      ██    ██ ██ ██  ██ ██ ██  ██ █████   ██         ██        █████   ██    ██ ██    ██ ██████  
██      ██    ██ ██  ██ ██ ██  ██ ██ ██      ██         ██        ██      ██    ██ ██    ██ ██   ██ 
 ██████  ██████  ██   ████ ██   ████ ███████  ██████    ██        ██       ██████   ██████  ██   ██ 
                                                                                                                                                                                          
    """)

# Setup
args = {
    'batch_size': 64,
    'numIters': 500,                                # Total number of training iterations
    'num_simulations': 100,                         # Total number of MCTS simulations to run when deciding on a move to play
    'numEps': 100,                                  # Number of full games (episodes) to run during each iteration
    'numItersForTrainExamplesHistory': 20,
    'epochs': 2,                                    # Number of epochs of training per iteration
    'checkpoint_path': 'latest.pth'                 # location to save latest set of weights
}
game = Connect4Game()
# model = MockModel(game)
mcts = MCTS(game)

# Start Game
board = game.get_init_board()
player = PLAYER_X
while True:
    
    node = mcts.search(board, player)
    board, player = node.board, node.player
    game.print_board(board)
    win, play = game.is_win(board)
    if win:
        if(play == PLAYER_X):
            print("X WINS!!!")
            break
        else:
            print("O WINS!!!")
            break
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
    board, player = game.get_next_state(board, player, user_input)

    win, play = game.is_win(board)
    if win:
        if(play == PLAYER_X):
            print("X WINS!!!")
            break
        else:
            print("O WINS!!!")
            break
    
    if(game.is_full_board(board)):
        print("DRAW")
        break