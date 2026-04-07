import numpy as np

# Opret et 3x3 bræt fyldt med nuller
board = np.zeros((3, 3), dtype=int)
print(board)

# Funktion til at lave et træk på brættet
def make_move(board, row, col, player):
    if board[row, col] == 0:
        board[row, col] = player
        return True
    return False

# Funktion til at tjekke om der er en vinder
def check_winner(board):
    for i in range(3):
        if np.all(board[i, :] == 1) or np.all(board[:, i] == 1):
            return 1
        if np.all(board[i, :] == 2) or np.all(board[:, i] == 2):
            return 2
    if np.all(np.diag(board) == 1) or np.all(np.diag(np.fliplr(board)) == 1):
        return 1
    if np.all(np.diag(board) == 2) or np.all(np.diag(np.fliplr(board)) == 2):
        return 2
    return 0

# spil loop
while True:
    row = int(input(f"Player {player}, enter row (0-2): "))
    col = int(input(f"Player {player}, enter column (0-2): "))
    
    if make_move(board, row, col, player):
        print(board)
        winner = check_winner(board)
        if winner != 0:
            print(f"Player {winner} wins!")
            break
        player = 2 if player == 1 else 1
    else:
        print("Invalid move. Try again.")
