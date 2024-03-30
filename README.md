# Connect-4-Reinforcement-learning

## Background and Motivation

Connect Four is a two players game which takes place on a 6x7 rectangular board placed vertically between them. One player has 21 blue coins and the other 21 red coins. Each player can drop a coin at the top of the board in one of the seven columns; the coin falls down and fills the lower unoccupied square. Of course a player cannot drop a coin in a certain column if it's already full (i.e. if it already contains six coins).

Even if there's no rule about who begins first, we assume, as in chess, that the darker side makes the first move. We also use the chess notation to represent a square on the board. That is, we number rows from 0 to 6 starting from the bottom and the columns from 5 to 0 starting from the leftmost.

## Problem Statement

The rules of the game are as follows:

- Every player tries to connect their coin type in a sequence of 4.
- After every move by any player, the status of the game is checked whether it is over. A game is considered over in the following scenarios:
- - Either of the players have 4 coins on the board in a sequence vertically, horizontally or diagonally.
- - The board is full that is after 42 moves none of the players got a sequence of 4. In this case the game is a tie.
- Using the above rules, the problem statement is to develop an AI using Reinforcement Learning and train it to play with human players and try to maximize the number of wins by the AI.

## Purpose/Motivation

The purpose/ motivation of this project is mainly to identify and understand the difference in implementation and results of Connect 4 using different agents.

## Methodology

### Environment

Connect4 Board

### Agent

To train the agent, select Train Computer in the main menu. It will play iterations games which was passed as an argument to the program.After training the computer, when 'vs Computer' option is selected, a human can play against the trained computer.Each time 'Train Computer' mode is selected, it trains from the beginning.
The state space is all the states which each player sees. For the first player it consists all the boards with an even number of disks, while for the second player it is all the boards with an odd number of disks.The action space will be the numbers 1–7 for each column a player can play.The reward will be 1 for winning, -1 for losing, 0.5 for a tie and 0 otherwise.
Note here that like in every 2-players’ game, the next state is not determined by the action taken because it depends also on the opponent’s action. The transition probability between 2 states depends on both the player’s and the opponent’s policies.

### Policies

The playing policy is e-greedy where the epsilon is chosen randomly.The epsilon factor determines whether to take a random move or an optimal move based on the Q function learnt.The discount factor decays after every iteration during training.In the beginning we have encouraged exploration (random values)Latter stage of training, we encouraged the computer to learn to play against more optimal players.

## Q-Learning

The state space is all the states which each player sees. For the first player it consists all the boards with even number of disks, while for the second player it is all the boards with odd number of disks.The action space will be the numbers 1–7 for each column a player can play.The reward will be 1 for winning, -1 for losing, 0.5 for a tie and 0 otherwise. The targets were calculated according to the Q learning algorithm:
Q(s,a) = Q(s,a) + α(max(Q(s’,a’))+gR-Q(s,a)) where Q is the Q function, s is the state, a is the action, α is the learning rate, R is the reward and g is the discount factor.

## DQN

The Neural network to approximate the Q-value function.The state is given as the input and the Q-value of all possible actions is generated as the output.The loss function here is mean squared error of the predicted Q-value and the target Q-value – Q\*.
