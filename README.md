# AITicTacToe 5x5
## Overview
This is an advanced Tic Tac Toe game: instead of just achieving one 3-in-a-row, the goal is to achieve as many 3-in-a-row combinations as possible on a 5x5 board. The game ends when only one position is left unoccupied. The winner is the player with the highest number of 3-in-a-row combinations.

The program features two players:

**Query Player (Human player):** You make decisions manually for your moves, given the remaining open spots on the board.
**Alpha-Beta AI Player:** A computer opponent that uses alpha-beta pruning to efficiently determine optimal moves.

## Rules
1. Players take turns placing their moves (X or O) on the board.
2. A 3-in-a-row can be formed horizontally, vertically, or diagonally.
3. The game ends when there is only one open space remaining.
4. The winner is the player with the most 3-in-a-row combinations.

## Setup and Installation
1. Ensure you have Python 3.7+ installed on your machine.
2. Clone this repository or download the program files.
3. Run the program using: ``` python Tic_Tac_Toe_5x5.py ```
