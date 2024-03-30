import random


class RandomAgent:

    def update(self, state, action, reward, next_state):
        pass

    def choose_action(self, env, state, valid_moves):
        return random.choice(valid_moves)
