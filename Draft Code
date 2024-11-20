//DRAFT DRAFT DRAFT


//Board Initialization**: The board is a 5x5 grid.
//Gameplay**: Players take turns placing 'X' and 'O' on the board until only one position is left.
//Winning Condition**: The player with the most 3-in-a-row sequences wins.
//Alpha-Beta Pruning**: The AI uses alpha-beta pruning to make optimal moves, focusing on creating 3-in-a-row sequences and switching to defense when necessary.




import random

# Initialize the board
board = [[' ' for _ in range(5)] for _ in range(5)]

# Function to print the board
def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 9)

# Function to check for 3-in-a-row
def check_three_in_a_row(board, player):
    count = 0
    # Check rows
    for row in board:
        if row.count(player) == 3 and row.count(' ') == 2:
            count += 1
    # Check columns
    for col in range(5):
        column = [board[row][col] for row in range(5)]
        if column.count(player) == 3 and column.count(' ') == 2:
            count += 1
    # Check diagonals
    diagonals = [
        [board[i][i] for i in range(5)],
        [board[i][4-i] for i in range(5)]
    ]
    for diag in diagonals:
        if diag.count(player) == 3 and diag.count(' ') == 2:
            count += 1
    return count

# Function to check if the board is full
def is_full(board):
    return all(cell != ' ' for row in board for cell in row)

# Function to get available moves
def get_available_moves(board):
    return [(r, c) for r in range(5) for c in range(5) if board[r][c] == ' ']

# Alpha-beta pruning algorithm
def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_full(board):
        return check_three_in_a_row(board, 'X') - check_three_in_a_row(board, 'O')
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_available_moves(board):
            r, c = move
            board[r][c] = 'X'
            eval = alpha_beta(board, depth-1, alpha, beta, False)
            board[r][c] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves(board):
            r, c = move
            board[r][c] = 'O'
            eval = alpha_beta(board, depth-1, alpha, beta, True)
            board[r][c] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Function to make the best move using alpha-beta pruning
def best_move(board):
    best_val = float('-inf')
    best_move = None
    for move in get_available_moves(board):
        r, c = move
        board[r][c] = 'X'
        move_val = alpha_beta(board, 3, float('-inf'), float('inf'), False)
        board[r][c] = ' '
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move

# Main game loop
def play_game():
    current_player = 'X'
    
    while not is_full(board):
        print_board(board)
        
        if current_player == 'X':
            r, c = best_move(board)
        else:
            available_moves = get_available_moves(board)
            r, c = random.choice(available_moves)
        
        board[r][c] = current_player
        
        current_player = 'O' if current_player == 'X' else 'X'
    
    print_board(board)
    
    x_score = check_three_in_a_row(board, 'X')
    o_score = check_three_in_a_row(board, 'O')
    
    print(f"X's score: {x_score}")
    print(f"O's score: {o_score}")
    
    if x_score > o_score:
        print("X wins!")
    elif o_score > x_score:
        print("O wins!")
    else:
        print("It's a tie!")

play_game()
```

This code sets up the game, handles the turns, and uses alpha-beta pruning to make optimal moves for the AI player. Feel free to run this code and let me know if you have any questions or need further modifications!
