from pprint import pprint


def Game(env, agent1, agent2):
    env.reset()
    while True:
        state = env.get_state()
        if env.player == 1:
            action = agent1.choose_action(
                env, state, [c for c in range(7) if env.is_valid_move(c)]
            )
            env.make_move(action)

            if env.check_winner(1):
                agent1.update(state, action, 1000, None)
                return 1
            elif env.is_draw():
                agent1.update(state, action, 10, None)
                return 0
            elif env.check_lose_next():
                agent1.update(state, action, -1000, env.get_state())
            else:
                agent1.update(state, action, -1, env.get_state())

        else:
            action = agent2.choose_action(
                env, state, [c for c in range(7) if env.is_valid_move(c)]
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
