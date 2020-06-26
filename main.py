import threading
import time
import sys
from os import path

import arcade
import numpy as np
import tensorflow as tf

# Fix for tensorflow and keras internal error
physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

from simulation.game import CarGame
from DQNAgent import DQNAgent


game: CarGame


def run_game():
    """Function which starts game.

    Run on new thread for app not to be locked.
    """
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    SCREEN_TITLE = 'Car Racer'
    global game
    game = CarGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.set_update_rate(1 / 60)
    game.set_vsync(True)
    arcade.run()


def write_stats(log, score):
    """Description of write_stats.

    Args:
       * log (str): Long string similar to the console displayed + average of 100
       * score (str): Current score of run + (optional) average of 100
    """
    
    file = open('log_no_2.txt', 'a')
    file.write('\n')
    file.write(log)
    file.close()

    file = open('log_score_no_2.txt', 'a')
    file.write('\n')
    file.write(score)
    file.close()


def main(filename='model.h5', load_file=False):
    """Main function of program."""

    thread = threading.Thread(target=run_game)
    thread.start()

    time.sleep(1)

    lr = 0.001
    observation_space, action_space = game.get_params()
    agent = DQNAgent(
        gamma=0.99,
        epsilon=0.01,
        lr=lr,
        input_dims=observation_space,
        n_actions=action_space,
        mem_size=10000000,
        batch_size=64,
        epsilon_end=0.00001,
        fname=filename)

    if load_file and path.exists(filename):
        print('openieng............')
        agent.load_model()
    
    scores = []
    run = 0

    while thread.is_alive():
        run += 1
        terminal = False
        score = 0
        state = game.reset()
        state = np.reshape(state, [1, observation_space])
        while not terminal and thread.is_alive():
            action = agent.choose_action(state)
            next_state, reward, terminal = game.get_state(action)
            next_state = np.reshape(next_state, [1, observation_space])
            if not terminal:
                score += reward
            agent.store_transition(state, action, reward, next_state, terminal)
            state = next_state
            agent.learn()
        scores.append(score)

        log = 'Run: ' + str(run) + ', epsilon: ' + \
            str(agent.epsilon) + ', score: ' + str(score)
        print(log)

        if run % 100 == 0:
            avg_score = np.mean(scores[-100:])
            scores.clear()
            log += ', avg_score: ' + str(avg_score)
            pts = str(score) + '  ' + str(avg_score)
            write_stats(log, pts)
            agent.save_model()


if __name__ == '__main__':
    # For some reason this improves TensorFlow speed
    tf.compat.v1.disable_eager_execution()

    if len(sys.argv) == 3:
        load_file = True if int(sys.argv[2]) != 0 else False
        main(sys.argv[1], load_file)
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()
