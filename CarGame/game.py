import arcade
from CarGame.car import Car
from CarGame.track import Track
from CarGame.helper import Helper
from shapely.geometry import LineString


# Main game class
class CarGame(arcade.Window):

    # Initialize window, initialize variables
    def __init__(self, width, height, title):
        super().__init__(width, height, title, False, True)
        arcade.set_background_color(arcade.color.WHITE)
        self.track = Track()
        self.car = Car(109, 528, 0.5, 0.5, 90, self.track)
        self.helper = Helper()
        self.color = arcade.color.GREEN
        self.points = 0
        self.terminal = False
        self.terminal_counter = 0


    # Render the screen
    def on_draw(self):
        arcade.start_render()

        # Draw track outer boundary
        arcade.draw_line_strip(
            self.track.trackOuterBoundary, arcade.color.BLACK)

        # Draw track inner boundary
        arcade.draw_line_strip(
            self.track.trackInnerBoundary, arcade.color.BLACK)

        # Draw car
        arcade.draw_rectangle_filled(
            self.car.x, self.car.y, 30, 14, self.color, self.car.rotation)

        ##### DEBUG DRAWING #####

        # Draw rays
        #arcade.draw_lines(self.car.get_rays(), arcade.color.GREEN)

        # Draw intersections
        # for intersection in self.car.get_ray_intersection_points():
        #     if intersection:
        #         arcade.draw_point(intersection[1][0], intersection[1][1], arcade.color.RED, 9)

        # Draw cookies
        #arcade.draw_lines(self.track.trackCookies, arcade.color.BLACK)

        # Draw car corners
        #arcade.draw_point(self.car.fL()[0], self.car.fL()[1], arcade.color.BLACK, 9)
        #arcade.draw_point(self.car.fR()[0], self.car.fR()[1], arcade.color.BLACK, 9)
        #arcade.draw_point(self.car.rL()[0], self.car.rL()[1], arcade.color.BLACK, 9)
        #arcade.draw_point(self.car.rR()[0], self.car.rR()[1], arcade.color.BLACK, 9)

        # Write text
        # distances = self.car.get_intersection_distances()
        # for i in range(0, 10):
        #     arcade.draw_text('{}: {}'.format(i, distances[i]), 10, i*15, arcade.color.BLACK, 12)
        #arcade.draw_text('Outer: '+str(self.track.trackOuterBoundary), 10,
        #                 10, arcade.color.BLACK, 12)
        #arcade.draw_text('Inner: '+str(self.track.trackInnerBoundary), 10,
        #                 30, arcade.color.BLACK, 12)
        #arcade.draw_text('Cookies: '+str(self.track.trackCookies), 10,
        #                 10, arcade.color.BLACK, 12)
        arcade.draw_text('Terminal: '+str(self.terminal_counter), 10,
                         10, arcade.color.BLACK, 12)
        arcade.draw_text('Points: '+str(self.points), 10,
                         30, arcade.color.BLACK, 12)

    # Handle mouse movement -> for track creation
    def on_mouse_press(self, x, y, button, modifiers):
        ##### DEBUG #####

        #if button == arcade.MOUSE_BUTTON_LEFT:
        #    self.track.trackOuterBoundary.append((x, y))
        #elif button == arcade.MOUSE_BUTTON_RIGHT:
        #    self.track.trackInnerBoundary.append((x, y))
        #if button == arcade.MOUSE_BUTTON_LEFT:
        #    self.track.trackCookies.append((x, y))
        pass

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
            self.exit()

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

        # Debug, for drawing track
        #if key == arcade.key.I:
        #    self.track.trackInnerBoundary = []
        #if key == arcade.key.O:
        #    self.track.trackOuterBoundary = []
        #if key == arcade.key.I:
        #    self.track.trackCookies = []
        #if key == arcade.key.O:
        #    self.track.trackCookies.pop()
        #    self.track.trackCookies.pop()

    # Handle screen updates
    def on_update(self, x):

        if self.terminal:
            self.terminal_counter += 1
        self.terminal = False
        # Check for collisions
        fr = self.car.fR()
        fl = self.car.fL()
        rr = self.car.rR()
        rl = self.car.rL()
        carLines = [LineString([fr, fl]), LineString(
            [rr, rl]), LineString([fr, rr]), LineString([fl, rl])]

        # Track outer boundary collision
        for section in zip(self.track.trackOuterBoundary, self.track.trackOuterBoundary[1:]):
            line = LineString([section[0], section[1]])
            for side in carLines:
                if side.intersects(line):
                    self.car.reset()
                    self.points = 0
                    self.terminal = True

        # Track inner boundary collision
        for section in zip(self.track.trackInnerBoundary, self.track.trackInnerBoundary[1:]):
            line = LineString([section[0], section[1]])
            for side in carLines:
                if side.intersects(line):
                    self.car.reset()
                    self.points = 0
                    self.terminal = True

        cookie = False

        # Cookie collsion
        for p1, p2 in zip(*[iter(self.track.trackCookies)]*2):
            line = LineString([p1, p2])
            for side in carLines:
                if side.intersects(line):
                    cookie = True

        if cookie and not self.helper.cookie:
            self.points += 10
            self.helper.cookie = True
        elif not cookie:
            self.helper.cookie = False

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
        if self.helper.A and self.car.velocity < 0:
            self.car.rotate(True)
        if self.helper.D and self.car.velocity > 0:
            self.car.rotate(True)
        if self.helper.D and self.car.velocity < 0:
            self.car.rotate(False)

        # Handle car position change
        self.car.y += self.car.get_shift_y(self.car.velocity)
        self.car.x += self.car.get_shift_x(self.car.velocity)

        ##### DEBUG #####

        # Loop car on border, just for lols and not losing the car
        #if self.car.x > self.get_size()[0]:
        #    self.car.x = 0
        #elif self.car.x < 0:
        #    self.car.x = self.get_size()[0]
        #if self.car.y > self.get_size()[1]:
        #    self.car.y = 0
        #elif self.car.y < 0:
        #    self.car.y = self.get_size()[1]

    def exit(self):
        arcade.window_commands.close_window()

    def press_W(self):
        self.helper.W = True

    def press_S(self):
        self.helper.S = True

    def press_A(self):
        self.helper.A = True

    def press_D(self):
        self.helper.D = True

    def release(self):
        self.helper.W = False
        self.helper.D = False
        self.helper.S = False
        self.helper.A = False

    def get_state(self):
        return self.car.get_intersection_distances(), self.points, self.terminal_counter
