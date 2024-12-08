import random
from collections import defaultdict

class Board(defaultdict):
    """
    A board has the player to move, a cached utility value, 
    and a dict of {(x, y): player} entries, where player is 'X' or 'O'.
    This is being used from the games4e.ipynb file in our class lessons with the following changes:
    - we create a 5x5 board instead of the typical 3x3
    - scores are tracked for both players
    """
    empty = '.'
    off = '#'
    
    def __init__(self, width=5, height=5, to_move='X', scores=None, **kwds):
        self.__dict__.update(width=width, height=height, to_move=to_move, scores=scores or {'X': 0, 'O': 0}, **kwds)
        
    def new(self, changes: dict, **kwds) -> 'Board':
        "Given a dict of {(x, y): contents} changes, return a new Board with the changes."
        board = Board(width=self.width, height=self.height, **kwds)
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off
            
    def __hash__(self): 
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)
    
    def __repr__(self):
        def row(y): return ' '.join(self[x, y] for x in range(self.width))
        return '\n'.join(map(row, range(self.height))) + '\n'

# Print the 5x5 tic-tac-toe board
def print_board(board): print(board)

# Check for 3-in-a-row
def check_three_in_a_row(board, player):
    count = 0
    # Check rows
    for r in range(board.height):
        row = [board[c, r] for c in range(board.width)]
        count += sum(1 for i in range(len(row) - 2) if row[i:i+3] == [player] * 3)
    # Check columns
    for c in range(board.width):
        column = [board[c, r] for r in range(board.height)]
        count += sum(1 for i in range(len(column) - 2) if column[i:i+3] == [player] * 3)
    # Check diagonals
    diagonals = [
        [board[i, i] for i in range(board.width)],        # Top-left to bottom-right
        [board[i, board.width - 1 - i] for i in range(board.width)]  # Top-right to bottom-left
    ]
    for diag in diagonals:
        count += sum(1 for i in range(len(diag) - 2) if diag[i:i+3] == [player] * 3)
    return count

# Check if the board is full
def is_full(board):
    return all(board[x, y] != board.empty for x in range(board.width) for y in range(board.height))

# Get a list of available moves on the board
def get_available_moves(board):
    return [(x, y) for x in range(board.width) for y in range(board.height) if board[x, y] == board.empty]

# Alpha-beta pruning algorithm
def alpha_beta(board, depth, alpha, beta, maximizing_player):
    # If depth=0 or the board is full, evaluate the board
    if depth == 0 or is_full(board):
        return check_three_in_a_row(board, 'X') - check_three_in_a_row(board, 'O')
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_available_moves(board):
            # evaluating moves recursively
            new_board = board.new({move: 'X'})
            eval = alpha_beta(new_board, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves(board):
             # evaluating moves recursively
            new_board = board.new({move: 'O'})
            eval = alpha_beta(new_board, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Find the best move using alpha-beta pruning
def best_move(board):
    best_val = float('-inf')
    best_move = None
    for move in get_available_moves(board):
        new_board = board.new({move: 'X'})
        move_val = alpha_beta(new_board, 3, float('-inf'), float('inf'), False)
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move

# Main game loop for the 5x5 Tic Tac Toe game
def play_game():
    # Initialize board
    board = Board(width=5, height=5, to_move='X')
    print_board(board)
    
    while not is_full(board):
        if board.to_move == 'O':  
            # User's turn
            while True:
                try:
                    user_input = input("Player O move: ")
                    move = tuple(map(int, user_input.strip("()").split(',')))
                    if move in get_available_moves(board):
                        # applying the move to the board
                        board = board.new({move: 'O'}, to_move='X')
                        break
                    print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid format. Enter as 'row,col'.")
            print(f"Player O move: {move}.")
        else:  
            # AI's turn
            move = best_move(board)
            print(f"Player X move: {move}.")
            # applying the move to the board
            board = board.new({move: 'X'}, to_move='O')
        
        print_board(board)
    
    # Game over, calculate and display final scores
    x_score = check_three_in_a_row(board, 'X')
    o_score = check_three_in_a_row(board, 'O')
    
    print(f"X's score: {x_score}")
    print(f"O's score: {o_score}")
    
    if x_score > o_score:
        print("AI wins!")
    elif o_score > x_score:
        print("You win!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()
