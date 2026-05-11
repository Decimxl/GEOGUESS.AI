import sys
import numpy as np
import pygame

def setup():
    global board, screen

    pygame.init()
    screen = pygame.display.set_mode((500,500))

    #laver en 3*3 matrix
    board = np.zeros((3, 3), dtype=int)
    print(board)
    return board

#vorse variabler vi bruger til at spile
winner = 0
player = 1  
shift_player = True

need_redraw = True

#color values
background_color_gray = (122,122,122) #707070
background_color_darkgray = (89,89,89) #595959
ui_color_black = (0,0,0) #000000
player1_color_blue = (6,23,145) #061791
player2_color_red = (189,0,0) #BD0000

 
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
        shift_player = True
    else:
        print("You can't make that move")
        shift_player = False
    
    if shift_player == True:
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
    return board

#dette er den som laver grafik i vorse ui
def grafiks():

    #faver skærmen mørek grå
    pygame.Surface.fill(screen,background_color_darkgray)

    #laver en kasse grå til vorse 3x3
    pygame.draw.rect(screen, background_color_gray, (50,50,400,400))

   
    #laver vorse 3x3 grid
    
    l = 0
    while l != 4: #stopper nå l bliver 4
        thickness = 6
        offset = 50

        #dette er vorse defination til start positionen for en linje.
        #hvor x1 er en lingin som bliver 133 støre for hver linje der bliver tejnet
        x1 = int(l * 133 + offset )
        y1 = int(0 + offset)

        #dette er vorse defination på slut postitionen for en linje.
        x2 = x1
        y2 = int(y1 + 400)

        #den der tenjer de vertiacale linjer
        pygame.draw.line(screen,ui_color_black,(x1,y1),(x2,y2), thickness)
        #den der tenjer de  vandrete linjer
        pygame.draw.line(screen,ui_color_black,(y1,x1),(y2,x2), thickness)
        #hæver l med 1 for at skift til den næste linje
        l += 1

def colision():
    global mus_pos

    mus_x ,mus_y = mus_pos

    for item in colision_box_list:
        pos1,pos2 = item.split(":")
        x1,y1 = pos1.split(",")
        x2,y2 = pos2.split(",")



    print(mus_x)
    print(mus_y)


def make_colision():
    global colision_box_list

    b = 0
    d = 0
    colision_box_list = []

    while d != 3:
        while b != 3:
            offset = 50

            x1 = int(b * 133 + offset)
            y1 = int(d * 133 + offset)

            x2 = int((b + 1) * 133 + offset)
            y2 = int((d + 1) * 133 + offset)

            
            colision_box_list.append(f"{x1},{y1}:{x2},{y2}")
            b += 1
        d += 1
        b = 0



make_colision()

#dette er vorse main game loop
running = True
while running:
    
    for event in pygame.event.get():
        
        # Lukning af spillet
        if event.type == pygame.QUIT:
            running = False

        # Håndter mussen
        if event.type == pygame.MOUSEBUTTONDOWN:
            mus_pos = pygame.mouse.get_pos()
            need_redraw = True
            colision()
        
        #håndter keydown (alså tastertur tryk)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #hvis der ikke er nogle vinder så forsætter den bare med at køre programet
    #if winner == 0:
        #play()
    

    if need_redraw:
        grafiks()
        pygame.display.flip()
        need_redraw = False

pygame.quit()
sys.exit()