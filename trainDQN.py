import torch

from Agents.DeepQNetworkAgent import DQNAgent
from Agents.Human import Human
from Agents.MiniMaxAgent import MiniMaxAgent
from Agents.QLearningAgent import QLearningAgent
from Agents.RandomAgent import RandomAgent
from Agents.SmartAgent import SmartAgent
from Util.Board import Board


def state_to_tensor(state):
    return torch.tensor(state, dtype=torch.float32).flatten()


def play_game(env, agent1, agent2):
    env.reset()
    while True:
        state = state_to_tensor(env.board)
        if env.player == 1:
            action = agent1.select_action(state)
            env.make_move(action)
            next_state = env.get_state()

            if env.check_winner(1):
                agent1.memory.push((state, action, 1000, None))
                agent1.optimize_model()
                return 1
            elif env.is_draw():
                agent1.memory.push((state, action, 1000, None))
                agent1.optimize_model()
                return 0
            elif env.check_lose_next():
                agent1.memory.push((state, action, -1000, state_to_tensor(next_state)))
                agent1.optimize_model()
            else:
                agent1.memory.push((state, action, -1, state_to_tensor(next_state)))
                agent1.optimize_model()

        else:
            action = agent2.choose_action(
                env, env.board, [c for c in range(7) if env.is_valid_move(c)]
            )
            env.make_move(action)
            if env.check_winner(2):
                agent2.update(state, action, 1000, None)
                return 2
            elif env.is_draw():
                agent2.update(state, action, 10, None)
                return 0
            elif env.check_lose_next():
                agent2.update(state, action, -1000, env.get_state())
            else:
                agent2.update(state, action, -1, env.get_state())


agent1 = DQNAgent()
agent1.restore("Bot/DQNbot_policy.pth", "Bot/DQNbot_target.pth")
# agent2 = MiniMaxAgent(2)
agent2 = SmartAgent()
# agent2 = Human()


num_episodes = 1000
wins = 0
for episode in range(1, num_episodes + 1):
    wins += 1 if play_game(Board(), agent1, agent2) == 1 else 0
    if episode % 50 == 0:
        print(episode, wins)
    agent1.update_target_network()

agent1.save("Bot/DQNbot_policy.pth", "Bot/DQNbot_target.pth")
