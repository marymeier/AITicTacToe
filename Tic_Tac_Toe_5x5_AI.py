import math
import random
from collections import defaultdict

infinity = math.inf

class Board(defaultdict):
    """A board has the player to move, a cached utility value, 
    and a dict of {(x, y): player} entries, where player is 'X' or 'O'.
    This is being used from our class lessons."""
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
def print_board(board):
    print(board)

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
def ab_best_move(board, player):
    #if X's turn, initial best val is very low bc we want to maximize the score
    #if O's turn, initial best val is very high bc we want to minimize the score
    best_val = -infinity if player == 'X' else infinity
    best_move = None
    
    for move in get_available_moves(board):
        #looping through each available move, making a new board based on current move
        new_board = board.new({move: player})
        #use alpha-beta to evaluate new board after move is made
        move_val = alpha_beta(new_board, 3, -infinity, infinity, player == 'O')
        #if move results in better score, update best_val and set best_move to current move
        if (player == 'X' and move_val > best_val) or (player == 'O' and move_val < best_val):
            best_val = move_val
            best_move = move
    return best_move

#Find the best move using minimax (for Player O)
def minimax(board, depth, maximizing_player):
    if depth == 0 or is_full(board): #terminal state
        return check_three_in_a_row(board, 'X') - check_three_in_a_row(board, 'O')
    
    if maximizing_player: #'X'
        max_eval = -infinity #starting with the lowest possible value
        #create a new board with X making the move, recursively call minimax, decreasing the depth & choosing max eval        
        for move in get_available_moves(board):
            new_board = board.new({move: 'X'})
            eval = minimax(new_board, depth-1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else: #'O'
        min_eval = infinity #starting with the highest possible value
        #create a new board with X making the move, recursively call minimax, decreasing the depth & choosing min eval 
        for move in get_available_moves(board):
            new_board = board.new({move: 'O'})
            eval = minimax(new_board, depth-1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def minimax_best_move(board, player):
    best_move = None
    best_val = -infinity if player == 'X' else infinity

    for move in get_available_moves(board):
        new_board = board.new({move: player})
        #evaluate move using minimax
        move_val = minimax(new_board, 3, player == 'O')
        if (player == 'X' and move_val > best_val) or (player == 'O' and move_val < best_val):
            best_val = move_val
            best_move = move

    print(f"Best move for {player}: {best_move}")
    return best_move

# Main game loop for two AI players
def play_game():
    ''' 
    In this game-play, we are testing the difference between minimax and alpha-beta pruning to see which algorithm produces the best results.
    Player X is using alpha-beta pruning while player O uses the minimax algorithm.
    '''
    
    board = Board(width=5, height=5, to_move='X')
    print_board(board)
    
    #continue the game while there is more than 1 open space left
    while sum(1 for x in range(board.width) for y in range(board.height) if board[x, y] == board.empty) > 1:
        if board.to_move == 'X':  
            #player X (alpha-beta pruning)
            move = ab_best_move(board, 'X')
        else:  
            #player O (minimax)
            move = minimax_best_move(board, 'O')
            
        print(f"Player {board.to_move} considering move: {move}")
        print(f"Player {board.to_move} move: {move}.")
        board = board.new({move: board.to_move}, to_move='O' if board.to_move == 'X' else 'X')
        print_board(board)
    
    #game ends with 1 space remaining
    print("Game over! Only one space left.")
    
    #calculate and print final scores
    x_score = check_three_in_a_row(board, 'X')
    o_score = check_three_in_a_row(board, 'O')
    
    print(f"X's score: {x_score}")
    print(f"O's score: {o_score}")
    
    if x_score > o_score:
        print("Player X (Alpha-Beta) wins!")
    elif o_score > x_score:
        print("Player O (Minimax) wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    play_game()