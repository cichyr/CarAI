import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model


class ReplayBuffer():
    def __init__(self, max_size, input_dims):
        self.mem_size = max_size
        self.mem_cntr = 0

        self.state_memory = np.zeros((self.mem_size, input_dims), dtype=np.int)
        self.new_state_memory = np.zeros((self.mem_size, input_dims), dtype=np.int)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.int32)

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


def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims, observation_space):
    model = keras.Sequential([
        keras.layers.Dense(fc1_dims, input_shape=(observation_space,), activation='relu'),
        keras.layers.Dense(fc2_dims, activation='relu'),
        keras.layers.Dense(n_actions, activation=None)
    ])

    model.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')

    return model


class DQNAgent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size, 
                input_dims, epsilon_dec=1e-9, epsilon_end=0.00001, 
                mem_size=1000000, fname='dqn_model.h5'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(lr, n_actions, input_dims, 256, 256, input_dims)

    def store_transition(self, state, action, reward, next_state, terminal):
        self.memory.store_transition(state, action, reward, next_state, terminal)

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            actions = self.q_eval.predict(state)

            action = np.argmax(actions)

        return action

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        states, next_states, actions, rewards, terminals = self.memory.sample_buffer(self.batch_size)

        #print(states)    
        #print(next_states)    
        q_eval = self.q_eval.predict(states)
        q_next = self.q_eval.predict(next_states)

        q_target = np.copy(q_eval)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        q_target[batch_index, actions] = rewards + self.gamma * np.max(q_next, axis=1) * terminals

        self.q_eval.train_on_batch(states, q_target)

        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_min else self.eps_min

    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)


# GAMMA = 0.95
# LEARNING_RATE = 0.005

# MEMORY_SIZE = 1000000
# BATCH_SIZE = 32

# OBSERVATION = 0#100
# LEARNING = 1000000

# EXPLORATION_MAX = 0.005#1
# EXPLORATION_MIN = 0.000005#0.229
# EXPLORATION_DECAY = (EXPLORATION_MAX - EXPLORATION_MIN)/LEARNING


# class DeepQNetwork:

#     def __init__(self, observation_space, action_space):
#         self.exploration_rate = EXPLORATION_MAX

#         self.action_space = action_space
#         self.memory = deque(maxlen=MEMORY_SIZE)

#         self.model = Sequential()
#         self.model.add(Dense(32, input_shape=(observation_space,), activation="relu"))
#         self.model.add(Dense(128, activation="relu"))
#         self.model.add(Dense(512, activation="relu"))
#         self.model.add(Dense(512, activation="relu"))
#         self.model.add(Dense(128, activation="relu"))
#         self.model.add(Dense(64, activation="relu"))
#         self.model.add(Dense(32, activation="relu"))
#         self.model.add(Dense(self.action_space, activation="linear"))
#         self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

#     def remember(self, state, action, reward, next_state, terminal):
#         self.memory.append((state, action, reward, next_state, terminal))

#     def act(self, state):
#         if np.random.rand() < self.exploration_rate:
#             return random.randrange(self.action_space)
#         q_values = self.model.predict(state)
#         #print(np.argmax(q_values[0]))
#         return np.argmax(q_values[0])

#     def experience_replay(self):
#         if len(self.memory) < BATCH_SIZE:
#             return
#         batch = random.sample(self.memory, BATCH_SIZE)
#         for state, action, reward, state_next, terminal in batch:
#             q_update = reward
#             if not terminal:
#                 q_update = (reward + GAMMA * np.amax(self.model.predict(state_next)[0]))
#             q_values = self.model.predict(state)
#             q_values[0][action] = q_update
#             self.model.fit(state, q_values, verbose=0)
#         self.exploration_rate -= EXPLORATION_DECAY
#         self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)