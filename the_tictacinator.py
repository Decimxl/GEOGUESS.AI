import gymnasium as gym
from gymnasium import spaces
import numpy as np


class DecisionChainEnv(gym.Env):

    def __init__(self):
        super().__init__()

        self.observation_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(9,),
            dtype=np.float32
        )
        self.action_space = spaces.Discrete(3)

        self.max_steps = 9
        self.step_count = 0
        self.state = np.zeros(self.observation_space.shape, dtype=self.observation_space.dtype)

    def reset(self, seed=None, options=None):
        self.step_count = 0
        self.state = np.zeros(self.observation_space.shape, dtype=self.observation_space.dtype)
        return self.state, {}

    def step(self, action):
        self.step_count += 1

        self.state = np.clip(
            self.state + (int(action) - 1) * 0.1,
            self.observation_space.low,
            self.observation_space.high
        )

        done = self.step_count >= self.max_steps
        reward = float(self.evaluate_chain()) if done else 0.0

        return self.state, reward, done, False, {}

    def evaluate_chain(self):
        return float(np.sum(self.state))
