import math


# Class representing car
class Car():

    # Initialize car values
    def __init__(self, x, y, acceleration, brake_force, rotation):
        self.__x = x
        self.x = x
        self.__y = y
        self.y = y
        self.acceleration = acceleration
        self.brake_force = brake_force
        self.deceleration = 0.25
        self.__rotation = rotation
        self.rotation = rotation
        self.velocity = 0
        self.__max_speed = 15
        self.__rotation_coef = 7
        self.braking = False

    def reset(self):
        self.x = self.__x
        self.y = self.__y
        self.rotation = self.__rotation
        self.velocity = 0

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

    # Get car corners (front Right, Left, rear Right, Left respectively)
    def fR(self):
        return (self.x + (15*math.cos(math.radians(self.rotation)) + 7*math.sin(math.radians(self.rotation))), self.y + (15*math.sin(math.radians(self.rotation)) - 7*math.cos(math.radians(self.rotation))))

    def fL(self):
        return (self.x + (15*math.cos(math.radians(self.rotation)) - 7*math.sin(math.radians(self.rotation))), self.y + (15*math.sin(math.radians(self.rotation)) + 7*math.cos(math.radians(self.rotation))))

    def rR(self):
        return (self.x + (-15*math.cos(math.radians(self.rotation)) + 7*math.sin(math.radians(self.rotation))), self.y + (-15*math.sin(math.radians(self.rotation)) - 7*math.cos(math.radians(self.rotation))))

    def rL(self):
        return (self.x + (-15*math.cos(math.radians(self.rotation)) - 7*math.sin(math.radians(self.rotation))), self.y + (-15*math.sin(math.radians(self.rotation)) + 7*math.cos(math.radians(self.rotation))))
