import numpy as np
import tensorflow as tf
from ReplayBuffer import ReplayBuffer
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam


class DQNAgent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size, 
                input_dims, epsilon_dec=1e-7, epsilon_end=0.00001, 
                mem_size=1000000, fname='dqn_model.h5'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = self.build_dqn(lr, n_actions, input_dims, 256, 256)

    def build_dqn(self, lr, n_actions, input_dims, fc1_dims, fc2_dims):
        model = keras.Sequential([
            keras.layers.Dense(fc1_dims, input_shape=(input_dims,), activation='relu'),
            keras.layers.Dense(fc2_dims, activation='relu'),
            keras.layers.Dense(n_actions, activation=None)
        ])
    
        model.compile(optimizer=Adam(learning_rate=lr), loss='mean_squared_error')
    
        return model

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
