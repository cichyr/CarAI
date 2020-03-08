import math


# Class representing car
class Car():

    # Initialize car values
    def __init__(self, x, y, acceleration, brake_force, rotation):

        self.x = x
        self.y = y
        self.acceleration = acceleration
        self.brake_force = brake_force
        self.deceleration = 0.25
        self.rotation = rotation
        self.velocity = 0
        self.__max_speed = 5#20
        self.__rotation_coef = 5#10
        self.braking = False

    # Get shift in Y axis
    def get_velocity_y(self):

        return self.velocity * math.sin(math.radians(self.rotation))

    # Get shift in X axis
    def get_velocity_x(self):

        return self.velocity * math.cos(math.radians(self.rotation))

    # Change car velocity
    def accelerate(self, accelerate: bool, brake: bool, forward: bool):

        # Acceleration
        if accelerate:
            if abs(self.velocity) < self.__max_speed and forward and not self.braking:
                self.velocity += self.acceleration
            elif abs(self.velocity) < self.__max_speed and not self.braking:
                self.velocity -= self.acceleration

        # Braking
        elif brake:
            if forward:
                self.velocity -= self.brake_force
            else:
                self.velocity += self.brake_force

        # Deceleration
        else:
            if forward:
                self.velocity -= self.deceleration
            else:
                self.velocity += self.deceleration

    def rotate(self, right: bool):

        # Turning right
        if right:
            self.rotation -= self.__rotation_coef

        # Turning left
        else:
            self.rotation += self.__rotation_coef

    def fR(self):
        return (self.x + (15*math.cos(math.radians(self.rotation)) + 7*math.sin(math.radians(self.rotation))), self.y + (15*math.sin(math.radians(self.rotation)) - 7*math.cos(math.radians(self.rotation))))

    def fL(self):
        return (self.x + (15*math.cos(math.radians(self.rotation)) - 7*math.sin(math.radians(self.rotation))), self.y + (15*math.sin(math.radians(self.rotation)) + 7*math.cos(math.radians(self.rotation))))
    
    def rR(self):
        return (self.x + (-15*math.cos(math.radians(self.rotation)) + 7*math.sin(math.radians(self.rotation))), self.y + (-15*math.sin(math.radians(self.rotation)) - 7*math.cos(math.radians(self.rotation))))

    def rL(self):
        return (self.x + (-15*math.cos(math.radians(self.rotation)) - 7*math.sin(math.radians(self.rotation))), self.y + (-15*math.sin(math.radians(self.rotation)) + 7*math.cos(math.radians(self.rotation))))