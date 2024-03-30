import random

import torch
import torch.nn as nn
import torch.optim as optim


class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, transition):
        self.memory.append(transition)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)


class DQNAgent:
    def __init__(
        self,
        input_size=42,
        hidden_size=128,
        output_size=7,
        gamma=0.99,
        epsilon=0.02,
        epsilon_decay=0.999,
        epsilon_min=0.01,
        learning_rate=0.1,
        memory_capacity=10000,
        batch_size=64,
    ):
        self.input_size = input_size
        self.output_size = output_size
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.memory = ReplayMemory(memory_capacity)
        self.policy_net = DQN(input_size, hidden_size, output_size)
        self.target_net = DQN(input_size, hidden_size, output_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=learning_rate)

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.output_size)
        else:
            with torch.no_grad():
                return self.policy_net(state).argmax().item()

    def optimize_model(self):
        if len(self.memory.memory) < self.batch_size:
            return
        transitions = self.memory.sample(self.batch_size)
        batch = list(zip(*transitions))
        state_batch = torch.stack(batch[0])
        action_batch = torch.tensor(batch[1], dtype=torch.int64)
        reward_batch = torch.tensor(batch[2], dtype=torch.float32)
        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch[3])), dtype=torch.bool
        )
        non_final_next_states = torch.stack([s for s in batch[3] if s is not None])

        state_action_values = self.policy_net(state_batch).gather(
            1, action_batch.unsqueeze(1)
        )

        next_state_values = torch.zeros(self.batch_size)
        next_state_values[non_final_mask] = (
            self.target_net(non_final_next_states).max(1)[0].detach()
        )

        expected_state_action_values = reward_batch + self.gamma * next_state_values

        loss = nn.functional.smooth_l1_loss(
            state_action_values.squeeze(), expected_state_action_values
        )

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.update_epsilon()

    def update_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def update_target_network(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())
    
    def save(self, policy_file, target_file):
        torch.save(self.policy_net.state_dict(), policy_file)
        torch.save(self.target_net.state_dict(), target_file)
    
    def restore(self, policy_file, target_file):
        self.policy_net.load_state_dict(torch.load(policy_file))
        self.target_net.load_state_dict(torch.load(target_file))
