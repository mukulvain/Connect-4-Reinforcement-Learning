from pprint import pprint


class Human:
    def __init__(self):
        print("Welcome Human!")

    def update(self, state, action, reward, new_state):
        print("You chose", action)
        pprint(new_state)
        print()

    def choose_action(self, env, state, valid_moves):
        pprint(state)
        print("\nFrom the following set of valid moves: ", valid_moves)
        return int(input("Enter a valid move: "))
