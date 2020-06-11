from shapely.geometry import LineString
from CarGame.track import Track
import math


# Class representing car
class Car():

    # Initialize car values
    def __init__(self, x, y, acceleration, brake_force, rotation, track):
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
        self.__max_speed = 10
        self.__rotation_coef = 7
        self.braking = False
        self.track = track

    # Reset car values
    def reset(self):
        self.x = self.__x
        self.y = self.__y
        self.rotation = self.__rotation
        self.velocity = 0

    # Get car seeing rays - 100 pixels each direction
    def get_rays(self):
        ray = 400
        rays = []
        fr = self.fR()
        fl = self.fL()
        rr = self.rR()
        rl = self.rL()

        # Front rays

        # Straight
        rays.append((fl[0]-(fl[0]-fr[0])/2, fl[1]-(fl[1]-fr[1])/2))
        rays.append((rays[-1][0]+self.get_shift_x(ray),
                     rays[-1][1]+self.get_shift_y(ray)))
        # Left 10*
        off = 10
        rays.append(fl)
        rays.append((rays[-1][0]+self.get_shift_x(ray, off),
                     rays[-1][1]+self.get_shift_y(ray, off)))
        # Left 45*
        off = 45
        rays.append(fl)
        rays.append((rays[-1][0]+self.get_shift_x(ray, off),
                     rays[-1][1]+self.get_shift_y(ray, off)))
        # Left 90*
        off = 90
        rays.append(fl)
        rays.append((rays[-1][0]+self.get_shift_x(ray, off),
                     rays[-1][1]+self.get_shift_y(ray, off)))
        # Right 10*
        off = -10
        rays.append(fr)
        rays.append((rays[-1][0]+self.get_shift_x(ray, off),
                     rays[-1][1]+self.get_shift_y(ray, off)))
        # Right 45*
        off = -45
        rays.append(fr)
        rays.append((rays[-1][0]+self.get_shift_x(ray, off),
                     rays[-1][1]+self.get_shift_y(ray, off)))
        # Right 90*
        off = -90
        rays.append(fr)
        rays.append((rays[-1][0]+self.get_shift_x(ray, off),
                     rays[-1][1]+self.get_shift_y(ray, off)))

        # Rear rays

        # Straight
        rays.append((rl[0]-(rl[0]-rr[0])/2, rl[1]-(rl[1]-rr[1])/2))
        rays.append((rays[-1][0]-self.get_shift_x(ray),
                     rays[-1][1]-self.get_shift_y(ray)))
        # Left 45*
        off = -45
        rays.append(rl)
        rays.append((rays[-1][0]-self.get_shift_x(ray, off),
                     rays[-1][1]-self.get_shift_y(ray, off)))
        # Right 45*
        off = 45
        rays.append(rr)
        rays.append((rays[-1][0]-self.get_shift_x(ray, off),
                     rays[-1][1]-self.get_shift_y(ray, off)))

        return rays

    # Returns intersection points
    def get_ray_intersection_points(self):
        intersection_points = []
        rays = self.get_rays()
        for i in range(0, 10):
            # Initial value
            intersection_points.append(False)
            prev_point = False

            # Get intersection with track outer boundary
            for section in zip(self.track.trackOuterBoundary, self.track.trackOuterBoundary[1:]):
                l1 = LineString([rays[i*2], rays[i*2 + 1]])
                l2 = LineString([section[0], section[1]])
                if l1.intersects(l2):
                    point = (l1.intersection(l2).x, l1.intersection(l2).y)
                    if (prev_point and self.calculate_length(rays[i*2], point) < self.calculate_length(rays[i*2], prev_point)) or not prev_point:
                        prev_point = point
                        intersection_points[i] = (rays[i*2], point)

            # Get intersection with track inner boundary
            for section in zip(self.track.trackInnerBoundary, self.track.trackInnerBoundary[1:]):
                l1 = LineString([rays[i*2], rays[i*2 + 1]])
                l2 = LineString([section[0], section[1]])
                if l1.intersects(l2):
                    point = (l1.intersection(l2).x, l1.intersection(l2).y)
                    if (prev_point and self.calculate_length(rays[i*2], point) < self.calculate_length(rays[i*2], prev_point)) or not prev_point:
                        prev_point = point
                        intersection_points[i] = (rays[i*2], point)

        return intersection_points

    # Get distances to intersections
    def get_intersection_distances(self):
        intersections = self.get_ray_intersection_points()
        distances = []

        # Get distance to intersection (segment length formula)
        for intersection in intersections:
            if intersection:
                distances.append(math.ceil(self.calculate_length(
                    intersection[0], intersection[1])))
            else:
                # They are too far apart
                distances.append(400)

        distances.append(self.x)
        distances.append(self.y)
        distances.append(self.velocity)
        return distances

    # Get shift in Y axis
    def get_shift_y(self, multiplier, offset=0):
        return multiplier * math.sin(math.radians(self.rotation+offset))

    # Get shift in X axis
    def get_shift_x(self, multiplier, offset=0):
        return multiplier * math.cos(math.radians(self.rotation+offset))

    def calculate_length(self, point1, point2):
        return math.sqrt(math.pow((point1[0] - point2[0]), 2) + math.pow((point1[1] - point2[1]), 2))

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
