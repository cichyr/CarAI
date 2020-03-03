import arcade
import os
import sys
import time


class MyGame(arcade.Window):
# Main game class        
        
    # Initialize window
    def __init__(self, width, height, title):
                    
        self.loop = True
        
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)

    # Prepare Tile Array
    def setup(self):
    
        self.on_draw()

    # Render the screen
    def on_draw(self):
        
        arcade.start_render()
        arcade.draw_rectangle_filled(420, 100, 45, 65, arcade.color.RED)

    # Handle user key press
    def on_key_press(self, key, modifiers):
    
        # Exit game
        if key == arcade.key.Q:
            arcade.window_commands.close_window()


# Main function
def main():

    # Global vars for easier edit
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    SCREEN_TITLE = "Car Racer"

    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == '__main__':
    main()


