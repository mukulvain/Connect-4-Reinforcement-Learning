import random
import math

class Node:
    def __init__(self, state, action, parent, player):
        self.state = state
        self.action = action
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_actions = [a for a in range(7) if state[0][a] == 0]
        self.player = player

    def select_child(self):
        return max(self.children, key=lambda c: c.wins / c.visits + 1.41 * (2 * math.log(self.visits) / c.visits) ** 0.5)

    def add_child(self, action, state, player):
        child = Node(state, action, self, 3 - player)
        self.children.append(child)
        self.untried_actions.remove(action)
        return child

    def update(self, reward):
        self.visits += 1
        self.wins += reward

    def best_action(self):
        return max(self.children, key=lambda c: c.visits).action
    
# Monte Carlo Tree Search (MCTS)
class MCTSAgent:
    def __init__(self, player, num_simulations=1000):
        self.player = player
        self.num_simulations = num_simulations

    def update(self, state, action, reward, next_state):
        pass

    def choose_action(self, env, state, valid_moves):
        root = Node(state, None, None, self.player)
        for _ in range(self.num_simulations):
            node = root
            env_copy = env.copy()
            # state_copy = state.copy()
            state_copy = state

            # Selection
            while node.untried_actions == [] and node.children != []:
                node = node.select_child()
                env_copy.step(node.action)
                # state_copy = env_copy.state
                state_copy = env_copy

            # Expansion
            if node.untried_actions != []:
                action = random.choice(node.untried_actions)
                env_copy.make_move(action)
                # state_copy = env_copy.state
                state_copy = env_copy
                node = node.add_child(action, state_copy, self.player)
            # Simulation
            while not env_copy.is_terminal():
                action = random.choice(env_copy.valid_moves)
                env_copy.step(action)
            reward = env_copy.get_reward(self.player)
            # Backpropagation
            while node is not None:
                node.update(reward)
                node = node.parent
        return root.best_action()