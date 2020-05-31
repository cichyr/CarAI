from CarGame.game import CarGame
import arcade
import threading
import keyboard
import time
import random


game = ""


def run_game():
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    SCREEN_TITLE = "Car Racer"
    global game
    game = CarGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.set_update_rate(1/60)
    game.set_vsync(True)
    arcade.run()


def action():
    choice = random.randint(1,8)
    if choice == 1:
        game.press_W()
    elif choice == 2:
        game.press_S()
    elif choice == 3:
        game.press_A()
    elif choice == 4:
        game.press_D()
    elif choice == 5:
        game.release_W()
    elif choice == 6:
        game.release_S()
    elif choice == 7:
        game.release_A()
    elif choice == 8:
        game.release_D()


def main():
    #thread = threading.Thread(target=run_game)
    #thread.start()
    #time.sleep(1)
    
    run_game()

    done = False
    epochs = 0

    while not True:#keyboard.is_pressed('q'):
        action()
        reward, done = game.get_state()

        epochs += 1
        time.sleep(0.01)

        if epochs%100 == 0:
            print("Epochs: {}".format(epochs))
        
        
if __name__ == '__main__':
    main()
