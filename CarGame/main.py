import arcade
from car import Car
from track import Track
from helper import Helper
from physics import Physics


# Main game class
class CarGame(arcade.Window):

    # Initialize window, initialize variables
    def __init__(self, width, height, title):
        super().__init__(width, height, title, False, True)
        arcade.set_background_color(arcade.color.WHITE)
        self.car = Car(714, 266, 0.5, 0.5, 180)
        self.track = Track()
        self.helper = Helper()
        self.physics = Physics()
        self.color = arcade.color.GREEN

    # Render the screen
    def on_draw(self):
        arcade.start_render()

        # Draw track outer boundary
        for section in zip(self.track.trackOuterBoundary, self.track.trackOuterBoundary[1:]):
            arcade.draw_line(
                section[0][0], section[0][1], section[1][0], section[1][1], arcade.color.BLACK)

        # Draw track inner boundary
        for section in zip(self.track.trackInnerBoundary, self.track.trackInnerBoundary[1:]):
            arcade.draw_line(
                section[0][0], section[0][1], section[1][0], section[1][1], arcade.color.BLACK)

        # Draw car
        arcade.draw_rectangle_filled(
            self.car.x, self.car.y, 30, 14, self.color, self.car.rotation)

        # Debug car corners drawing
        #arcade.draw_point(self.car.fL()[0], self.car.fL()[1], arcade.color.BLACK, 9)
        #arcade.draw_point(self.car.fR()[0], self.car.fR()[1], arcade.color.BLACK, 9)
        #arcade.draw_point(self.car.rL()[0], self.car.rL()[1], arcade.color.BLACK, 9)
        #arcade.draw_point(self.car.rR()[0], self.car.rR()[1], arcade.color.BLACK, 9)

        # Debug text writing
        arcade.draw_text('Outer: '+str(self.track.trackOuterBoundary), 10,
                         10, arcade.color.BLACK, 12)
        arcade.draw_text('Inner: '+str(self.track.trackInnerBoundary), 10,
                         30, arcade.color.BLACK, 12)

    # Handle mouse movement -> for track creation
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.track.trackOuterBoundary.append((x,y))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.track.trackInnerBoundary.append((x,y))

    # Handle user key press
    def on_key_press(self, key, modifiers):

        # Car movement keys
        if key == arcade.key.W:
            self.helper.W = True
            if self.car.velocity < 0:
                self.car.braking = True
        if key == arcade.key.S:
            self.helper.S = True
            if self.car.velocity > 0:
                self.car.braking = True
        if key == arcade.key.A:
            self.helper.A = True
        if key == arcade.key.D:
            self.helper.D = True

        if key == arcade.key.SPACE:
            self.car.velocity = 0

        # Exit game
        if key == arcade.key.Q:
            arcade.window_commands.close_window()

    # Handle user key release
    def on_key_release(self, key, modifiers):

        # Car movement keys
        if key == arcade.key.W:
            self.helper.W = False
            self.car.braking = False
        if key == arcade.key.S:
            self.helper.S = False
            self.car.braking = False
        if key == arcade.key.A:
            self.helper.A = False
        if key == arcade.key.D:
            self.helper.D = False
        if key == arcade.key.I:
            self.track.trackInnerBoundary = []
        if key == arcade.key.O:
            self.track.trackOuterBoundary = []

    # Handle screen updates
    def on_update(self, x):

        # Check for collisions
        carList = [self.car.fR(), self.car.fL(), self.car.rL(), self.car.rR(), self.car.fR()]
        if self.physics.getCollisions(carList, self.track.trackOuterBoundary) or self.physics.getCollisions(carList, self.track.trackInnerBoundary):
            self.color = arcade.color.RED
        else:
            self.color = arcade.color.GREEN

        # Handle car velocity change
        if self.helper.W and self.car.velocity >= 0:
            self.car.accelerate(True, False, True)
        elif self.helper.W and self.car.velocity < 0:
            self.car.accelerate(False, True, False)
        elif self.helper.S and self.car.velocity > 0:
            self.car.accelerate(False, True, True)
        elif self.helper.S and self.car.velocity <= 0:
            self.car.accelerate(True, False, False)

        if not self.helper.W and self.car.velocity > 0:
            self.car.accelerate(False, False, True)
        elif not self.helper.S and self.car.velocity < 0:
            self.car.accelerate(False, False, False)

        # Handle car rotation
        if self.helper.A and self.car.velocity > 0:
            self.car.rotate(False)
        if self.helper.D and self.car.velocity > 0:
            self.car.rotate(True)

        # Handle car position change
        self.car.y += self.car.get_velocity_y()
        self.car.x = self.car.x + self.car.get_velocity_x()

        # Loop car on border, just for lols and not losing the car
        if self.car.x > self.get_size()[0]:
            self.car.x = 0
        elif self.car.x < 0:
            self.car.x = self.get_size()[0]
        if self.car.y > self.get_size()[1]:
            self.car.y = 0
        elif self.car.y < 0:
            self.car.y = self.get_size()[1]


# Main function
def main():
    # Global vars for easier edit
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    SCREEN_TITLE = "Car Racer"

    CarGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == '__main__':
    main()
