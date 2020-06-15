from CarGame.game import CarGame
import arcade
import threading
import keyboard
import time
import random
import numpy as np
import tensorflow as tf
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


game = ""


GAMMA = 0.9
LEARNING_RATE = 0.001

MEMORY_SIZE = 1000000
BATCH_SIZE = 32

OBSERVATION = 0#100
LEARNING = 100000

EXPLORATION_MAX = 0.5#1
EXPLORATION_MIN = 0.0001#0.229
EXPLORATION_DECAY = (EXPLORATION_MAX - EXPLORATION_MIN)/LEARNING


class DeepQNetwork:

    def __init__(self, observation_space, action_space):
        self.exploration_rate = EXPLORATION_MAX

        self.action_space = action_space
        self.memory = deque(maxlen=MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(observation_space,), activation="relu"))
        self.model.add(Dense(128, activation="relu"))
        self.model.add(Dense(128, activation="relu"))
        self.model.add(Dense(128, activation="relu"))
        self.model.add(Dense(64, activation="relu"))
        self.model.add(Dense(32, activation="relu"))
        self.model.add(Dense(self.action_space, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

    def remember(self, state, action, reward, next_state, terminal):
        self.memory.append((state, action, reward, next_state, terminal))

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space)
        q_values = self.model.predict(state)
        #print(np.argmax(q_values[0]))
        return np.argmax(q_values[0])

    def experience_replay(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update = (reward + GAMMA * np.amax(self.model.predict(state_next)[0]))
            q_values = self.model.predict(state)
            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)
        self.exploration_rate -= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)


def run_game():
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    SCREEN_TITLE = "Car Racer"
    global game
    game = CarGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.set_update_rate(1/60)
    game.set_vsync(True)
    arcade.run()


def main():
    #run_game()
    thread = threading.Thread(target=run_game)
    thread.start()
    time.sleep(1)
    
    #print(state)

    observation_space = 15
    action_space = 4

    dqn = DeepQNetwork(observation_space, action_space)
    run = 0

    while True:
        run += 1
        state = game.reset()
        state = np.reshape(state, [1, observation_space])
        reward_old = 0
        while True:
            action = dqn.act(state)
            state_next, reward, terminal = game.get_state(action)
            reward = reward if not terminal else -reward_old
            state_next = np.reshape(state_next, [1, observation_space])
            dqn.remember(state, action, reward, state_next, terminal)
            state = state_next
            if terminal:
                print("Run: " + str(run) + ", exploration: " + str(dqn.exploration_rate) + ", score: " + str(reward_old))
                break
            reward_old = reward
            if run > OBSERVATION:
                dqn.experience_replay()


if __name__ == '__main__':
    main()
