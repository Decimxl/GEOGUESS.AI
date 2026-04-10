import numpy as np

#makes a 3 *3 grid
board = np.zeros((3, 3), dtype=int)
print(board)

winner = 0
player = 1  

def play():
    global player, win1 , win2,winner

    play = input(f"player {player} a move row:col")

    try:
        row,col = map(int, play.split(":"))
    except ValueError:
        print("invalid input")
        return

    if board[row,col] == 0:
        board[row,col] = player
    else:
        print("You can't make that move")
        
    i = 0
    while i != 3:
        if np.all(board[i,:] == player):
            print (f"player {player} win")
            winner = player
        if np.all(board[:,i] == player):
            print (f"player {player} win")
            winner = player
        if np.all(np.diag(board) == player):
            print(f"player {player} win")
            winner = player
        if np.all(np.diag(np.fliplr(board)) == player):
            print(f"player {player} win")
            winner = player

        i += 1 

    if np.all(board != 0):
        winner = "draw"

    if player == 1:
        player = 2
    elif player == 2:
        player = 1

        
    print(board)

while winner == 0:
    play()