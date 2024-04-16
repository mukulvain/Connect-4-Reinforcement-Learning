import numpy as np


class Board:
    def __init__(self):
        # Standard 6 X 7 Game
        self.board = np.zeros((6, 7), dtype=int)
        self.winning_sets = self.generate_winning_sets()
        # Player 1 Starts
        self.player = 1

    def generate_winning_sets(self):
        # Generate all possible winning sets (horizontal, vertical, diagonal)
        winning_sets = []

        # Horizontal
        for r in range(6):
            for c in range(4):
                winning_sets.append(set([(r, c + i) for i in range(4)]))
        # Vertical
        for r in range(3):
            for c in range(7):
                winning_sets.append(set([(r + i, c) for i in range(4)]))

        # Diagonal (positive slope)
        for r in range(3):
            for c in range(4):
                winning_sets.append(set([(r + i, c + i) for i in range(4)]))
        # Diagonal (negative slope)
        for r in range(3):
            for c in range(3, 7):
                winning_sets.append(set([(r + i, c - i) for i in range(4)]))
        return winning_sets

    def is_valid_move(self, column):
        # If the top cell in that column is empty
        return 0 <= column < 7 and self.board[0][column] == 0

    def make_move(self, column):
        # The coin is dropped in the bottom most cell in a column
        invalid = True
        for r in range(5, -1, -1):
            if self.board[r][column] == 0:
                self.board[r][column] = self.player
                invalid = False
                # break
                return r,column
        if not invalid:
            self.player = 3 - self.player  # Switch player

    def check_lose_next(self):
        for move in range(7):
            if self.is_valid_move(move):
                for r in range(5, -1, -1):

                    if self.board[r][move] == 0:
                        self.board[r][move] = self.player
                    else:
                        continue

                    if self.check_winner(self.player):
                        self.board[r][move] = 0
                        return True
                    else:
                        self.board[r][move] = 0
                        break
        return False

    def check_winner(self, player):
        for winning_set in self.winning_sets:
            if all(self.board[r][c] == player for (r, c) in winning_set):
                return True
        return False

    def is_draw(self):
        # When the board gets full
        return all(self.board[0][c] != 0 for c in range(7))

    def get_state(self):
        return tuple(map(tuple, self.board))

    def reset(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.player = 1
