import numpy as np


class ReplayBuffer():
    def __init__(self, max_size, input_dims):
        self.mem_size = max_size
        self.mem_cntr = 0

        self.state_memory = np.zeros((self.mem_size, input_dims), dtype=np.int)
        self.new_state_memory = np.zeros((self.mem_size, input_dims), dtype=np.int)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.int)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.int)

    def store_transition(self, state, action, reward, next_state, terminal):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = next_state
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = int(1-terminal)
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        next_states = self.new_state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        terminals = self.terminal_memory[batch]

        return states, next_states, actions, rewards, terminals
