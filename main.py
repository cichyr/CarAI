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


GAMMA = 0.95
LEARNING_RATE = 0.001

MEMORY_SIZE = 1000000
BATCH_SIZE = 32

OBSERVATION = 100
LEARNING = 8000

EXPLORATION_MAX = 1
EXPLORATION_MIN = 0.0001
#EXPLORATION_DECAY = (EXPLORATION_MAX - EXPLORATION_MIN)/LEARNING


class DeepQNetwork:

    def __init__(self, observation_space, action_space):
        self.exploration_rate = EXPLORATION_MAX

        self.action_space = action_space
        self.memory = deque(maxlen=MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Dense(40, input_shape=(observation_space,), activation="relu"))
        self.model.add(Dense(80, activation="relu"))
        self.model.add(Dense(80, activation="relu"))
        self.model.add(Dense(40, activation="relu"))
        self.model.add(Dense(20, activation="relu"))
        self.model.add(Dense(self.action_space, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

    def remember(self, state, action, reward, next_state, terminal):
        self.memory.append((state, action, reward, next_state, terminal))

    def act(self, state, observation):
        if (np.random.rand() < self.exploration_rate) or observation:
            return random.randrange(self.action_space)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def experience_replay(self):
        pass



def run_game():
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    SCREEN_TITLE = "Car Racer"
    global game
    game = CarGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.set_update_rate(1/60)
    game.set_vsync(True)
    arcade.run()


def do_action(choice):
    game.release()
    if choice == 0:
        game.press_W()
    elif choice == 1:
        game.press_S()
    elif choice == 2:
        game.press_A()
    elif choice == 3:
        game.press_D()


def main():
    #run_game()
    thread = threading.Thread(target=run_game)
    thread.start()
    time.sleep(1)
    
    #print(state)

    observation_space = 10
    action_space = 4

    dqn = DeepQNetwork(observation_space, action_space)
    run = 0
    ctr = 0
    terminal = False

    while True:
        run += 1
        state, reward, t_ctr = game.get_state()
        state = np.reshape(state, [1, observation_space])
        step = 0
        while True:
            terminal = False
            step += 1
            action = dqn.act(state, True)
            do_action(action)
            state_next, reward, t_ctr = game.get_state()
            if t_ctr != ctr:
                terminal = True
                ctr = t_ctr
            reward = reward if not terminal else -reward
            state_next = np.reshape(state_next, [1, observation_space])
            dqn.remember(state, action, reward, state_next, terminal)
            state = state_next
            if terminal:
                print("Run: " + str(run) + ", exploration: " + str(dqn.exploration_rate) + ", score: " + str(step))
                #score_logger.add_score(step, run)
                break
            if ctr > OBSERVATION:
                dqn.experience_replay()


if __name__ == '__main__':
    main()
