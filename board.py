import numpy as np

#makes a 3 *3 grid
board = np.zeros((3, 3), dtype=int)
print(board)

#test board
test = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

player = 1  

def play():
    global player

    play = input(f"player {player} a move row:col")

    row,col = map(int, play.split(":"))
    
    if board[row,col] == 0:
        board[row,col] = player

        if player == 1:
            player = 2
        elif player == 2:
            player = 1
    else:
        print("You can't make that move")
        
    print(board)

def colision(row,col):

while np.all != 0:

    play()