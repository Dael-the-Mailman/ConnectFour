import numpy as np

class Node:
    def __init__(self, board, game, player, parent=None):
        self.board = board
        self.game = game
        self.player = player
        
        win, _ = self.game.is_win(board)
        if win or self.game.is_full_board(board):
            self.is_terminal = True
        else:
            self.is_terminal = False
        
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.visits = 0 
        self.score = 0
        self.children = {}

# idk how to test this 😛
class MCTS:
    def __init__(self, game, num_iter=1600):
        self.game = game
        self.num_iter = num_iter

    def search(self, initial_state, initial_player):
        self.root = Node(initial_state, self.game, initial_player)

        for _ in range(self.num_iter):
            node = self.select(self.root)
            score = self.rollout(node)

            self.backpropagate(node, score)

        try:
            return self.get_best_move(self.root, 0)
        except:
            pass

    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)

            else:
                return self.expand(node)

        return node

    def expand(self, node):
        valid_moves = node.game.get_valid_moves()
        for move in valid_moves:
            if move not in node.children:
                new_node = Node(node.board, node.game, node)
                node.children[move] = new_node

                if len(valid_moves) == len(node.children):
                    node.is_fully_expanded = True

            return new_node
        
        print("Big oopsie")
    
    def rollout(self, node):
        board = node.board
        player = node.player
        while True:
            win, _ = node.game.is_win(board)
            if win:
                return node.game.get_reward(board, player)
            
            if node.game.is_full_board(board):
                return 0
            
            valid_moves = node.game.get_valid_moves()
            probs = valid_moves/valid_moves.sum()
            move = np.random.choice(range(self.game.get_action_space()), p=probs)
            board, player = node.game.get_next_state(board, player, move)
        
        print("Big oopsie") 

    def backpropagate(self, node, score):
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    def get_best_move(self, node, exploration_constant):
        best_score = float('-inf')
        best_moves = []

        for child_node in node.children.values():
            current_player = child_node.player
            move_score = current_player * child_node.score / child_node.visits + \
                               exploration_constant * np.sqrt(np.log(node.visits / child_node.visits))

            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]
            
            elif move_score == best_score:
                best_moves.append(child_node)

        return np.random.choice(best_moves)

