from stable_baselines3 import PPO
from the_tictacinator import DecisionChainEnv

env = DecisionChainEnv()

model = PPO(
    "MlpPolicy",
    env,
    verbose=1
)

model.learn(total_timesteps=100000)

model.save("decision_agent")