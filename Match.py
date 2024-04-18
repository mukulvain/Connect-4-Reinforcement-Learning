import pickle

from Agents.Human import Human
from Agents.MiniMaxAgent import MiniMaxAgent
from Agents.QLearningAgent import QLearningAgent
from Agents.RandomAgent import RandomAgent
from Agents.SmartAgent import SmartAgent
from Agents.MCTS import MCTSAgent
from Util.Board import Board
from Util.Game import Game

with open("Bot/bot.pkl", "rb") as f:
    bot2 = pickle.load(f)

agent1 = QLearningAgent(bot2)
# agent1 = MCTSAgent(1)
agent2 = MiniMaxAgent(2)

test_env = Board()

games = 100
agent1_wins = 0
agent2_wins = 0
for i in range(games):
    winner = Game(test_env, agent1, agent2)
    if winner == 1:
        agent1_wins += 1
    elif winner == 2:
        agent2_wins += 1
    test_env.reset()

print(agent1_wins / games)
print(agent2_wins / games)
