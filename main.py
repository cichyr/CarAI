from CarGame.game import CarGame
import arcade
import threading
import keyboard
import time
import random
from NeuralNetwork import DeepQNetwork
import numpy as np
import tensorflow as tf


game = ''


def run_game():
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    SCREEN_TITLE = 'Car Racer'
    global game
    game = CarGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.set_update_rate(1/60)
    game.set_vsync(True)
    arcade.run()


def average(scoreboard):
    return sum(scoreboard)/len(scoreboard)


def write_stats(log, score):
    file = open('log.txt', 'a')
    file.write('\n')
    file.write(log)
    file.close()

    file = open('log_score.txt', 'a')
    file.write('\n')
    file.write(score)
    file.close()


def main():
    #run_game()
    thread = threading.Thread(target=run_game)
    thread.start()
    time.sleep(1)
    
    #print(state)
    lr = 0.001
    #n_games = 500
    observation_space, action_space = game.get_params()
    agent = DQNAgent(gamma=0.99, epsilon=0.01, lr=lr, input_dims=observation_space,
                n_actions=action_space, mem_size=1000000, batch_size=64, 
                epsilon_end=0.00001, fname='dqn_model_3.h5')
    agent.load_model()
    scores = []
    eps_history = []

    run = 0
    #scoreboard = []

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
            score += reward
            agent.store_transition(state, action, reward, next_state, terminal)
            state = next_state
            agent.learn()
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        log = 'Run: ' + str(run) + ', epsilon: ' + str(agent.epsilon) + ', score: ' + str(score)
        print(log)

        if run % 100 == 0:
            log +=  ', avg_score: ' + str(avg_score)
            pts = str(score) + '  ' + str(avg_score)
            write_stats(log, pts)
            agent.save_model()


if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()
    main()


# def main():
#     #run_game()
#     thread = threading.Thread(target=run_game)
#     thread.start()
#     time.sleep(1)
    
#     #print(state)

#     observation_space, action_space = game.get_params()

#     dqn = DeepQNetwork(observation_space, action_space)
#     run = 0
#     scoreboard = []

#     while thread.is_alive():
#         run += 1
#         state = game.reset()
#         state = np.reshape(state, [1, observation_space])
#         points = 0
#         while thread.is_alive():
#             action = dqn.act(state)
#             state_next, reward, terminal = game.get_state(action)
#             #reward = reward if not terminal else -reward_old
#             #print(reward)
#             if not terminal:
#                 points += reward
#             state_next = np.reshape(state_next, [1, observation_space])
#             dqn.remember(state, action, reward, state_next, terminal)
#             state = state_next
#             if terminal:
#                 scoreboard.append(points)
#                 print('Run: ' + str(run) + ', exploration: ' + str(dqn.exploration_rate) + ', score: ' + str(points))
#                 if run % 100 == 0 and run > 0:
#                     avg = average(scoreboard)
#                     scoreboard.clear()
#                     log = 'Run: ' + str(run) + ', exploration: ' + str(dqn.exploration_rate) + ', score: ' + str(points) + ', avg: ' + str(avg)
#                     write_stats(log, str(avg))

#                 break
#             dqn.experience_replay()


# if __name__ == '__main__':
#     main()
