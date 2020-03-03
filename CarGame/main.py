import arcade
import os
import sys
import time
import math


class Car():

    def __init__(self, x, y, acceleration, deceleration, rotation):
        self.x = x
        self.y = y
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.rotation = rotation
        self.velocity = 0

    def get_velocity_y(self):
        return self.velocity * math.sin(math.radians(self.rotation))

    def get_velocity_x(self):
        return self.velocity * math.cos(math.radians(self.rotation))


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
        self.car = Car(300, 50, 0.1, 0.2, 90)
        self.helper = Helper()

    # Prepare Tile Array
    def setup(self):

        self.on_draw()

    # Render the screen
    def on_draw(self):

        arcade.start_render()

        arcade.draw_rectangle_filled(
            self.car.x, self.car.y, 65, 45, arcade.color.RED, self.car.rotation)

    # Handle user key press
    def on_key_press(self, key, modifiers):

        # Car movement    
        if key == arcade.key.W:
            self.helper.W = True
        if key == arcade.key.S:
            self.helper.S = True
        if key == arcade.key.A:
            self.helper.A = True
        if key == arcade.key.D:
            self.helper.D = True

        # Strafe left/right for now
        #elif key == arcade.key.A:
        #    self.car.x -= 10
        #elif key == arcade.key.D:
        #    self.car.x += 10

        # Exit game
        if key == arcade.key.Q:
            arcade.window_commands.close_window()

    # Handle user key release
    def on_key_release(self, key, modifiers):
        
        # Car movement
        if key == arcade.key.W:
            self.helper.W = False
        if key == arcade.key.S:
            self.helper.S = False
        if key == arcade.key.A:
            self.helper.A = False
        if key == arcade.key.D:
            self.helper.D = False

    # Handle screen updates
    def on_update(self, x):
        
        # Handle car velocity change
        if self.helper.W and self.car.velocity >= 0:
            self.car.velocity += self.car.acceleration
        if self.helper.W and self.car.velocity < 0:
            self.car.velocity += self.car.deceleration
        if self.helper.S and self.car.velocity > 0:
            self.car.velocity -= self.car.deceleration
        if self.helper.S and self.car.velocity <= 0:
            self.car.velocity -= self.car.acceleration
        # Handle car rotation
        if self.helper.A:
            self.car.rotation += 5
        if self.helper.D:
            self.car.rotation -= 5

        # Handle car position change
        self.car.y += self.car.get_velocity_y()
        self.car.x += self.car.get_velocity_x()

        # Loop car on border, just for lols and not losing the car
        if self.car.x > self.get_size()[0]:
            self.car.x = 0
        elif self.car.x < 0:
            self.car.x = 600
        if self.car.y > self.get_size()[1]:
            self.car.y = 0
        elif self.car.y < 0:
            self.car.y = 600

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
