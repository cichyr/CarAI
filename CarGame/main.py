import arcade
import os
import sys
import time


class Car():

    def __init__(self, x, y, a, d):
        self.x = x
        self.y = y
        self.acceleration = a
        self.deceleration = d
        self.velocity = 0


class Helper():

    def __init__(self):
        self.W = False
        self.S = False
        self.A = False
        self.D = False


# Main game class
class CarGame(arcade.Window):

    # Initialize window
    def __init__(self, width, height, title):

        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.car = Car(300, 50, 0.1, 0.2)
        self.helper = Helper()
        #self.old = True
        self.old = False

    # Prepare Tile Array
    def setup(self):

        self.on_draw()

    # Render the screen
    def on_draw(self):

        arcade.start_render()

        arcade.draw_rectangle_filled(
            self.car.x, self.car.y, 45, 65, arcade.color.RED)

    # Handle user key press
    def on_key_press(self, key, modifiers):

        # Car movement    
        if key == arcade.key.W:
            self.helper.W = True
        elif key == arcade.key.S:
            self.helper.S = True
        elif key == arcade.key.A:
            self.helper.A = True
        elif key == arcade.key.D:
            self.helper.D = True

        # Strafe left/right for now
        elif key == arcade.key.A:
            self.car.x -= 10
        elif key == arcade.key.D:
            self.car.x += 10

        # Exit game
        elif key == arcade.key.Q:
            arcade.window_commands.close_window()

    # Handle user key release
    def on_key_release(self, key, modifiers):
        
        # Car movement
        if key == arcade.key.W:
            self.helper.W = False
        elif key == arcade.key.S:
            self.helper.S = False
        elif key == arcade.key.A:
            self.helper.A = False
        elif key == arcade.key.D:
            self.helper.D = False

    # Handle screen updates
    def on_update(self, x):
        
        # Handle car velocity change
        if self.helper.W and self.car.velocity >= 0:
            self.car.velocity += self.car.acceleration
        elif self.helper.W and self.car.velocity < 0:
            self.car.velocity += self.car.deceleration
        elif self.helper.S and self.car.velocity > 0:
            self.car.velocity -= self.car.deceleration
        elif self.helper.S and self.car.velocity <= 0:
            self.car.velocity -= self.car.acceleration

        # Handle car position change (TODO xD)
        self.car.y += self.car.velocity

        self.on_draw()


# Main function
def main():

    # Global vars for easier edit
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    SCREEN_TITLE = "Car Racer"

    game = CarGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()
