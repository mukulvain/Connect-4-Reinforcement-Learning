import random


class SmartAgent:

    def update(self, state, action, reward, next_state):
        pass

    def choose_action(self, env, state, valid_moves):
        for move in valid_moves:
            for r in range(5, -1, -1):

                if env.board[r][move] == 0:
                    env.board[r][move] = env.player
                else:
                    continue

                if env.check_winner(env.player):
                    env.board[r][move] = 0
                    return move
                else:
                    env.board[r][move] = 0
                    break
        return random.choice(valid_moves)
