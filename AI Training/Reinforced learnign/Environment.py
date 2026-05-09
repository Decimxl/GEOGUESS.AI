import numpy as np
import gymnasium as gym
from gymnasium import spaces
import random

# Enviroment til tic tac toe spillet. Lavet som en klasse som arver fra gym.Env. Det er her vi definerer vores action space og observation space, samt vores step og reset funktioner.
class TicTacToeEnv(gym.Env): 
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super().__init__()
        # Action space er 9 mulige moves (0-8) som repræsenterer de 9 felter på brættet
        # 0 1 2
        # 3 4 5
        # 6 7 8
        
        self.action_space = spaces.Discrete(9) # fortæller vores ai at den har 9 mulige træk på en tom spilleplade
        # værdier til brættet er: 
        # 0 for tomt
        # 1 for spiller x 
        # 2 for spiller o
        self.observation_space = spaces.Box(
            low=0,
            high=2,
            shape=(3,3),
            dtype=np.int8
        ) # definerer spillepladen som en 3x3 matrix hvor hver celle kan være 0, 1 eller 2. en action som i øverste venstre hjørne vil være [0,0]

        self.board = np.zeros((3,3), dtype=np.int8) # initialiserer spillepladen som en 3x3 matrix fyldt med 0'er
        self.player = random.choice([1, 2]) # starter med spiller 1 (x) kan evt ændres til 2 for at starte med spiller o

    def reset(self, seed=None, options=None): # seed er får at beholde vores miljø og options er ikke nødvendigt
        super().reset(seed=seed)
        self.board = np.zeros((3,3), dtype=np.int8)
        self.player = random.choice([1, 2]) # det er tilfældigt hvilken spiller der starter, det gør træningen mere robust fordi ai'en skal lære at spille mod både x og o
        return self.board.copy(), {} # nulstiller brættet og starter med spiller 1 (x) og returnerer den initiale observation (det tomme bræt) og en tom info dictionary

    def step(self, action):
        # action er et tal mellem 0 og 8 som repræsenterer det felt på brættet hvor spilleren vil placere sin brik
        # dette skal konverteres til row og col for at opdatere brættet korrekt
        row = action // 3 # laver action til row
        col = action % 3 # laver action til col

        # tjekker om move er gyldig (dvs. at det valgte felt er tomt)
        if self.board[row, col] != 0:
            reward = -2 # giver ai smæk med pisk fordi den er dum
            terminated = True # afslutter spillet fordi det er en ulovlig handling
            truncated = False # truncated er ikke relevant her fordi vi afslutter spillet ved en ulovlig handling
            return self.board.copy(), reward, terminated, truncated, {
                "Ulovlig handling": True,
                "player": self.player
            } # gemmer tilstanden

        # lav en handling på brættet
        self.board [row, col] = self.player # opdaterer brættet med spillerens træk

        # tjekker for sejr
        if self.check_win(self.player):
            reward = 1 # giver ai en belønning for at vinde
            terminated = True # afslutter spil
            truncated = False # truncated er ikke relevant her fordi vi afslutter spillet ved en sejr
            return self.board.copy(), reward, terminated, truncated, {
                "Vinder": self.player    
            } # gemmer tilstanden
        
        # tjekker for uafgjort
        if np.all(self.board != 0):
            reward = 0.1 # lille belønning for at spille til uafgjort i stedet for at tabe
            terminated = True # afslutter spillet ved uafgjort
            truncated = False # truncated er ikke relevant her fordi vi afslutter spillet ved uafgjort
            return self.board.copy(), reward, terminated, truncated, {
                "Uafgjort": True    
            } # gemmer tilstanden
        
        # næste move
        reward = 0 # ingen belønning for et normalt træk
        terminated = False # spillet fortsætter
        truncated = False # truncated er ikke relevant her fordi spillet fortsætter

        # skifter mellem spillerne
        self.player = 2 if self.player == 1 else 1 # skifter mellem spiller 1 og spiller 2

        return self.board.copy(), reward, terminated, truncated, {} # gemmer tilstanden
    
    def check_win(self, player):
        board = self.board
        # tjekker rækker
        for i in range(3):
            if np.all(board[i, :] == player):
                return True
        # tjekker kolonner
        for j in range(3):
            if np.all(board[:, j] == player):
                return True
        # tjekker diagonaler
        if np.all(np.diag(board) == player):
            return True
        # tjekker anti-diagonal
        if np.all(np.diag(np.fliplr(board)) == player):
            return True
        return False
    
    def render(self): # render funktionen viser brættet i konsollen på en læsbar måde
        symbols = {
            0: ".",
            1: "X",
            2: "O"
        }

        for row in self.board:
            print(" ".join(symbols[int(cell)] for cell in row))
        print()
    
    def available_actions(self):
        return [
            i for i, cell in enumerate(self.board.flatten()) 
            if cell == 0
        ]

