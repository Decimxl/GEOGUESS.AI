import random
import pickle
import numpy as np 

class QLearningAgent:
    def __init__(self, name, alpha=0.1, gamma=0.95, epsilon=1):
        self.name = name # agentens navn
        self.qtable = {} # Q-table for at gemme state-action værdier
        self.alpha = alpha # hvor meget agenten opdaterer sin Q-table baseret på nye erfaringer
        self.gamma = gamma # hvor meget agenten værdsætter fremtidige belønninger i forhold til umiddelbare belønninger
        self.epsilon = epsilon # sandsynligheden for at agenten vælger en tilfældig handling i stedet for den handling, der har den højeste Q-værdi

    def get_state(self, board): # konverterer brættet til en tuple, så det kan bruges som en nøgle i Q-table
        return tuple(board.flatten())
    
    def get_q_values(self, state):  # henter Q-værdier for en given tilstand, hvis tilstanden ikke findes i Q-table, initialiseres den med 0 for alle handlinger
        if state not in self.qtable:
            self.qtable[state] = np.zeros(9) # initialiserer Q-værdier for alle handlinger til 0
        return self.qtable[state]
    
    def choose_action(self, board, training=True): # vælger en handling baseret på epsilon-greedy strategi
        state = self.get_state(board) # henter state fra get_state
        q_values = self.get_q_values(state) # henter Q-værdier for den givne state

        available_actions = [
            i for i, cell in enumerate(board.flatten()) 
            if cell == 0
        ]

        if training and random.random() < self.epsilon: # hvis agenten er i træning og en tilfældig værdi er mindre end epsilon, vælg en tilfældig handling
            return random.choice(available_actions)
        
        return max(
            available_actions, 
            key=lambda action: q_values[action]
            )
    
    def learn(self, old_board, action, reward, new_board, terminated):
        old_state = self.get_state(old_board) # henter old_state fra get_state
        new_state = self.get_state(new_board) # henter new_state fra get_state
        
        old_q_values = self.get_q_values(old_state) # henter old_q_value for den givne old_state
        new_q_values = self.get_q_values(new_state) # henter new_q_value for den givne new_state

        old_q = old_q_values[action] # henter old_q for den givne action i old_q_values

        if terminated: # hvis spillet er afsluttet
            target = reward # sæt target til den modtagne belønning
        else: # hvis spillet ikke er afsluttet
            target = reward + self.gamma * np.max(new_q_values) # sæt target til den modtagne belønning plus den maksimale fremtidige belønning

        old_q_values[action] = old_q + self.alpha * (target - old_q) # opdater Q-værdien for den givne action i old_q_values baseret på læringsraten og forskellen mellem target og old_q

    def save(self, filename): # gemmer Q-table til en fil ved hjælp af pickle
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        
    @staticmethod
    def load(filename): # indlæser Q-table fra en fil ved hjælp af pickle
        with open(filename, 'rb') as file:
            return pickle.load(file)