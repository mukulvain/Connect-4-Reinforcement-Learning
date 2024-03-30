import math
import random

import numpy as np


class MiniMaxAgent:
    def __init__(self, player_num):
        self.winning_sets = []
        self.player = player_num

        # Horizontal
        for r in range(6):
            for c in range(4):
                self.winning_sets.append(set([(r, c + i) for i in range(4)]))
        # Vertical
        for r in range(3):
            for c in range(7):
                self.winning_sets.append(set([(r + i, c) for i in range(4)]))

        # Diagonal (positive slope)
        for r in range(3):
            for c in range(4):
                self.winning_sets.append(set([(r + i, c + i) for i in range(4)]))
        # Diagonal (negative slope)
        for r in range(3):
            for c in range(3, 7):
                self.winning_sets.append(set([(r + i, c - i) for i in range(4)]))

    def update(self, state, action, reward, new_state):
        pass

    def evaluate_window(self, window, player):
        score = 0
        opposite = 3 - player

        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opposite) == 3 and window.count(0) == 1:
            score -= 4
        return score

    def score(self, state, player):
        score = 0

        ## Center Column
        center_array = [int(i) for i in list(state[:, 3])]
        center_count = center_array.count(player)
        score += center_count * 3

        # Horizontal
        for r in range(6):
            row_array = [int(i) for i in list(state[r, :])]
            for c in range(4):
                window = row_array[c : c + 4]
                score += self.evaluate_window(window, player)
        # Vertical
        for c in range(7):
            col_array = [int(i) for i in list(state[:, c])]
            for r in range(3):
                window = col_array[r : r + 3]
                score += self.evaluate_window(window, player)

        # Diagonal (positive slope)
        for r in range(3):
            for c in range(4):
                window = [state[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player)
        # Diagonal (negative slope)
        for r in range(3):
            for c in range(4):
                window = [state[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, player)

        return score

    def get_valid_moves(self, state):
        return [col for col in range(7) if state[0][col] == 0]

    def move(self, state, column, player):
        for r in range(5, -1, -1):
            if state[r][column] == 0:
                state[r][column] = player
                break

    def is_draw(self, state):
        return all(state[0][c] != 0 for c in range(7))

    def check_winner(self, state, player):
        for winning_set in self.winning_sets:
            if all(state[r][c] == player for (r, c) in winning_set):
                return True
        return False

    def minimax(self, state, depth, alpha, beta, maximise):
        valid_moves = self.get_valid_moves(state)
        if self.check_winner(state, self.player):
            return (None, 100000)
        elif self.check_winner(state, 3 - self.player):
            return (None, -100000)
        elif self.is_draw(state):
            return (None, 0)
        elif depth == 0:
            return (None, self.score(state, self.player))

        if maximise:
            val = -math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                state_copy = state.copy()
                self.move(state_copy, col, self.player)
                new_score = self.minimax(state_copy, depth - 1, alpha, beta, False)[1]
                if new_score > val:
                    val = new_score
                    column = col
                alpha = max(new_score, alpha)
                if beta <= alpha:
                    break
            return column, val
        else:
            val = math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                state_copy = state.copy()
                self.move(state_copy, col, 3 - self.player)
                new_score = self.minimax(state_copy, depth - 1, alpha, beta, True)[1]
                if new_score < val:
                    val = new_score
                    column = col
                beta = min(beta, new_score)
                if beta <= alpha:
                    break
            return column, val

    def choose_action(self, env, state, valid_moves):
        action, val = self.minimax(np.array(state), 2, -math.inf, math.inf, True)
        return action
