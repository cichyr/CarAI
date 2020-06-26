import arcade
from .car import Car
from .track import Track
from .helper import Helper
from shapely.geometry import LineString


# Main game class
class CarGame(arcade.Window):

    # Initialize window, initialize variables
    def __init__(self, width=1920, height=1080, title='CarGame'):
        super().__init__(width, height, title, False, True)
        arcade.set_background_color(arcade.color.WHITE)
        self.track = Track()
        self.car = Car(109, 528, 0.5, 0.5, 90, self.track)
        self.helper = Helper()
        self.color = arcade.color.GREEN
        self.terminal = False
        self.cookie_counter = 0
        self.cookie_counter_old = 0

    # Render the screen
    def on_draw(self):
        arcade.start_render()

        # Draw track outer boundary
        arcade.draw_line_strip(
            self.track.track_outer_boundary, arcade.color.BLACK)

        # Draw track inner boundary
        arcade.draw_line_strip(
            self.track.track_inner_boundary, arcade.color.BLACK)

        # Draw car
        arcade.draw_rectangle_filled(
            self.car.x, self.car.y, 30, 14, self.color, self.car.rotation)

        ##### DEBUG DRAWING #####

        # Draw rays
        # arcade.draw_lines(self.car.get_rays(), arcade.color.GREEN)

        # Draw intersections
        # for intersection in self.car.get_ray_intersection_points():
        #     if intersection:
        #         arcade.draw_point(intersection[1][0], intersection[1][1], arcade.color.RED, 9)

        # Draw cookies
        # arcade.draw_lines(self.track.track_cookies, arcade.color.BLACK)

        # Draw car corners
        # arcade.draw_point(self.car.fL()[0], self.car.fL()[1], arcade.color.BLACK, 9)
        # arcade.draw_point(self.car.fR()[0], self.car.fR()[1], arcade.color.BLACK, 9)
        # arcade.draw_point(self.car.rL()[0], self.car.rL()[1], arcade.color.BLACK, 9)
        # arcade.draw_point(self.car.rR()[0], self.car.rR()[1], arcade.color.BLACK, 9)

        # Write text
        # distances = self.car.get_intersection_distances(0)
        # for i in range(0, 10):
        #     arcade.draw_text('{}: {}'.format(i, distances[i]), 10, i*15, arcade.color.BLACK, 12)
        # arcade.draw_text('Outer: '+str(self.track.track_outer_boundary), 10,
        #                  10, arcade.color.BLACK, 12)
        # arcade.draw_text('Inner: '+str(self.track.track_inner_boundary), 10,
        #                  30, arcade.color.BLACK, 12)
        # arcade.draw_text('Cookies: '+str(self.track.track_cookies), 10,
        #                  10, arcade.color.BLACK, 12)
        # arcade.draw_text('Terminal: '+str(self.terminal_counter), 10,
        #                  10, arcade.color.BLACK, 12)
        # arcade.draw_text('Points: '+str(self.points), 10,
        #                  30, arcade.color.BLACK, 12)

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

    # Handle screen updates
    def on_update(self, x):

        self.color = arcade.color.GREEN

        #self.terminal = False
        # Check for collisions
        fr = self.car.fR()
        fl = self.car.fL()
        rr = self.car.rR()
        rl = self.car.rL()
        carLines = [LineString([fr, fl]), LineString(
            [rr, rl]), LineString([fr, rr]), LineString([fl, rl])]

        # Track outer boundary collision
        for section in zip(self.track.track_outer_boundary, self.track.track_outer_boundary[1:]):
            line = LineString([section[0], section[1]])
            for side in carLines:
                if side.intersects(line):
                    self.terminal = True

        # Track inner boundary collision
        for section in zip(self.track.track_inner_boundary, self.track.track_inner_boundary[1:]):
            line = LineString([section[0], section[1]])
            for side in carLines:
                if side.intersects(line):
                    self.terminal = True

        if not self.terminal:
            cookie = False

            awaited_cookie = int((self.cookie_counter % 49))

            # Cookie collsion
            if not self.helper.cookie:
                line = LineString([self.track.track_cookies[awaited_cookie * 2], self.track.track_cookies[(awaited_cookie * 2) + 1]])
                for side in carLines:
                    if side.intersects(line):
                        cookie = True

            if cookie and not self.helper.cookie:
                #self.points += 100
                self.cookie_counter += 1
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

    def reset(self):
        #self.points = 0
        self.cookie_counter = 0
        self.cookie_counter_old = 0
        self.terminal = False
        self.car.reset()
        return self.car.get_intersection_distances()

    def do_action(self, choice):
        self.release()
        if choice == 0:
            self.helper.W = True
        elif choice == 1:
            self.helper.S = True
        elif choice == 2:
            #self.press_W()
            self.helper.A = True
        elif choice == 3:
            #self.press_W()
            self.helper.D = True       

    def release(self):
        self.helper.W = False
        self.helper.D = False
        self.helper.S = False
        self.helper.A = False

    def get_state(self, action):
        """Returns game state

        Args:
            action (int): Action returned by NN

        Returns:
            List(int): State
            int: Rewars
            bool: Terminal
        """
        self.do_action(action)
        reward = 0
        if self.car.velocity == 0.0 and (self.helper.A or self.helper.D):
            reward = -1
        if self.cookie_counter != self.cookie_counter_old:
            self.cookie_counter_old = self.cookie_counter
            reward = 100
        if self.terminal:
            reward = -1000
        return self.car.get_intersection_distances(), reward, self.terminal

    def get_params(self):
        return len(self.car.get_intersection_distances()), 4
