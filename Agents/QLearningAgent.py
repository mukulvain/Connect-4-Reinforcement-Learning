import pickle
import random


class QLearningAgent:
    def __init__(self, q_values={}, epsilon=0.2, alpha=0.8, gamma=1.0):
        self.q_values = q_values

        self.epsilon = epsilon  # Epsilon-Greedy
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor

    def get_q_value(self, state, action):
        # If the state is uninitialized, return 0
        return self.q_values.get((state, action), 0)

    def get_max_random(self, arr):
        # Function to get index of the maximum value
        max_val = max(arr)
        vals = [i for i in range(len(arr)) if arr[i] == max_val]
        # Return random index in case of a tie
        random.shuffle(vals)
        return vals[0]

    def update(self, state, action, reward, next_state):
        old_q_value = self.get_q_value(state, action)
        new_q_values = [self.get_q_value(next_state, a) for a in range(7)]
        best_next_action = self.get_max_random(new_q_values)

        # Bellman Equation
        new_q_value = old_q_value + self.alpha * (
            reward
            + self.gamma * self.get_q_value(next_state, best_next_action)
            - old_q_value
        )
        self.q_values[(state, action)] = new_q_value

    def choose_action(self, env, state, valid_moves):
        if random.random() < self.epsilon:
            return random.choice(valid_moves)
        else:
            values = [self.get_q_value(state, a) for a in valid_moves]
            return self.get_max_random(values)

    def save(self, name):
        with open(name, "wb") as f:
            pickle.dump(self.q_values, f)

    def restore(self, name):
        with open(name, "wb") as f:
            self.q_values = pickle.load(f)
