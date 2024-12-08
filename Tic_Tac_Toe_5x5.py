from collections import defaultdict
import math

infinity = math.inf

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

#Print the 5x5 tic-tac-toe board
def print_board(board): print(board)

#Check for 3-in-a-row
def check_three_in_a_row(board, player):
    count = 0
    #check rows
    for r in range(board.height):
        row = [board[c, r] for c in range(board.width)]
        count += sum(1 for i in range(len(row) - 2) if row[i:i+3] == [player] * 3)
    
    #check columns
    for c in range(board.width):
        column = [board[c, r] for r in range(board.height)]
        count += sum(1 for i in range(len(column) - 2) if column[i:i+3] == [player] * 3)
   
    #check diagonals
    diagonals = [
        #top-left to bottom-right
        [board[i, i] for i in range(board.width)],        
        #top-right to bottom-left
        [board[i, board.width - 1 - i] for i in range(board.width)]  
    ]
    
    for diag in diagonals:
        count += sum(1 for i in range(len(diag) - 2) if diag[i:i+3] == [player] * 3)
    return count

#Check if the board is full
def is_full(board):
    return all(board[x, y] != board.empty for x in range(board.width) for y in range(board.height))

#Get available moves
def get_available_moves(board):
    #returning a list of all empty positions on the board."""
    available_moves = []
    
    for x in range(board.width):
        for y in range(board.height):
            if board[x, y] == board.empty:  #checking if position is empty
                available_moves.append((x, y))
    return available_moves

#Alpha-beta pruning algorithm
def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_full(board): #terminal state
        #if terminal state is reached, return the final score
        return check_three_in_a_row(board, 'X') - check_three_in_a_row(board, 'O')
    
    if maximizing_player: #'X'
        max_eval = -infinity #starting with the lowest possible value
        for move in get_available_moves(board):
            new_board = board.new({move: 'X'})
            #create a new board with X making the move, recursively call alpha-beta, decreasing the depth and minimizing the player's turn
            eval = alpha_beta(new_board, depth-1, alpha, beta, False)
            #updating max_eval to be the higher value
            max_eval = max(max_eval, eval)
            #alpha=best value for the maximizing player
            alpha = max(alpha, eval)
            #pruning: break the loop early if beta <= alpha bc further moves won't affect the final move result
            if beta <= alpha:
                break
        return max_eval
    else: #'O'
        min_eval = infinity #starting with the highest possible value
        for move in get_available_moves(board):
            new_board = board.new({move: 'O'})
            #create a new board with O making the move, recursively call alpha-beta, decreasing the depth and maximizing the player's turn
            eval = alpha_beta(new_board, depth-1, alpha, beta, True)
            #updating min_eval to be lower value
            min_eval = min(min_eval, eval)
            #beta=best value for minimizing player
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

#Find the best move using alpha-beta pruning
def best_move(board):
    best_val = -infinity
    best_move = None
    
    for move in get_available_moves(board):
        #looping through each available move, making a new board based on current move
        new_board = board.new({move: 'X'})
        #use alpha-beta to evaluate new board after move is made
        move_val = alpha_beta(new_board, 3, -infinity, infinity, False)
        #if move results in better score, update best_val and set best_move to current move
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move

#Main game loop for the 5x5 Tic Tac Toe game
def play_game():
    #initialize board
    board = Board(width=5, height=5, to_move='X')
    print_board(board)
    
    while not is_full(board):
        if board.to_move == 'O':  
            #user's turn
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
            #AI's turn
            move = best_move(board)
            print(f"Player X move: {move}.")
            #applying the move to the board
            board = board.new({move: 'X'}, to_move='O')
        
        print_board(board)
    
    #game ends with 1 space remaining
    print("Game over! Only one space left.")
    
    #calculate and print final scores
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
