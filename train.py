from Agents.QLearningAgent import QLearningAgent
from Agents.RandomAgent import RandomAgent
from Agents.SmartAgent import SmartAgent
from Agents.MiniMaxAgent import MiniMaxAgent
from Util.Board import Board
from Util.Game import Game
import pickle


# Training the agent
agent1 = QLearningAgent()
agent1.restore("Bot/bot.pkl")
agent2 = SmartAgent()


num_episodes = 1000

wins = 0
for episode in range(num_episodes):
    wins += 1 if Game(Board(), agent1, agent2) == 1 else 0

print(wins / num_episodes)
agent1.save("Bot/bot.pkl")
