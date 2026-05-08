import gymnasium as gym
from gymnasium import spaces
import numpy as np


class DecisionChainEnv(gym.Env):

    def __init__(self):
        super().__init__()

        self.observation_space = spaces.Box(
            board_pos_00=0,
            board_pos_01=0,
            board_pos_02=0,
            board_pos_10=0,
            board_pos_11=0,
            board_pos_12=0,
            board_pos_20=0,
            board_pos_21=0,
            board_pos_22=0,
            dtype=np.int8
        )
        
        self.action_space = spaces.Discrete(3)

        self.max_steps = 9
        self.step_count = 0

    def reset(self, seed=None, options=None):
        self.step_count = 0

        self.state = np.random.uniform(0,0,0,0,0,0,0,0,0)

        return self.state, {}

    def step(self, action):

        self.step_count += 1

        # Update state (example rule)
        self.state = self.state + (action - 1) * 0.1

        done = self.step_count >= self.max_steps

        reward = 0

        if done:
            reward = self.evaluate_chain()

        return self.state, reward, done, False, {}

    def evaluate_chain(self):

        # reward logic (example)
        return float(np.sum(self.state))
