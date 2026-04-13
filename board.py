import numpy as np
import pygame

def setup():
    global board, screen

    pygame.init()
    screen = pygame.display.set_mode((500,500))

    #laver en 3*3 matrix
    board = np.zeros((3, 3), dtype=int)
    print(board)

#vorse variabler vi bruger til at spile
winner = 0
player = 1  

setup()

def play():
    global player, win1 , win2, winner

    #spilers input
    play = input(f"player {player} a move row:col")

    #spliter input til row og columes
    #hvis ikke inputet er gyldig så siger den at inputet er udgyldig
    try:
        row,col = map(int, play.split(":"))
    except ValueError:
        print("invalid input")
        return

    #setter enten 1 eller 2  basret på spileren hvis ik der alredere er en.
    if board[row,col] == 0:
        board[row,col] = player
    else:
        print("You can't make that move")
    
    #dette er vorse win loop som cheker om der er nolge på stripe
    i = 0
    while i != 3:
        #cheker om der er nogle lodret på stripe
        if np.all(board[i,:] == player):
            print (f"player {player} win")
            winner = player
        #cheker om der er nogle vandret på stripe
        if np.all(board[:,i] == player):
            print (f"player {player} win")
            winner = player
        ##cheker om der er nogle digonalt på stripe
        if np.all(np.diag(board) == player):
            print(f"player {player} win")
            winner = player
        if np.all(np.diag(np.fliplr(board)) == player):
            print(f"player {player} win")
            winner = player
        #forsætter loopet
        i += 1 

    #hvis helle bordet er fyldt så er det lige
    if np.all(board != 0):
        winner = "draw"

    #skifter mellem spilerne
    if player == 1:
        player = 2
    elif player == 2:
        player = 1
 
    print(board)


def grafiks():
    pygame.draw.rect()


#dette er vorse main game loop
running = True
while running:
    for event in pygame.event.get():
        # Lukning af spillet
        if event.type == pygame.QUIT:
            running = False

        # Håndter mussen
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
        
        #håndter keydown (alså tastertur tryk)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #hvis der ikke er nogle vinder så forsætter den bare med at køre programet
    """if winner == 0:
        play()"""
