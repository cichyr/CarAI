# Class representing track and collisions
class Track():

    # Initialize variables (track points)
    def __init__(self):
        self.track = [[960, 1080], [960, 590]]
        pass

    # Determinant of 3x3 Matrix (last column is 1).
    #   Formula: x1y2 + x2y3 + x3y1 - x3y2 - x1y3 - x2y1
    def determinant(self, p1, p2, p3):
        return p1[0]*p2[1] + p2[0]*p3[1] + p3[0]*p1[1] - p3[0]*p2[1] - p1[0]*p3[1] - p2[0]*p1[1]

    # Checking if point is on track line
    def pointOnSection(self, point1, point2, point3):

        # Point is on same line as section if determinant is equal 0
        if self.determinant(point1, point2, point3) == 0:
            # Checking if point is on section
            if min(point1[0], point2[0]) <= point3[0]:
                if point3[0] <= max(point1[0], point2[0]):
                    if min(point1[1], point2[1]) <= point3[1]:
                        if point3[1] <= max(point1[1], point2[1]):
                            return True

        # Point is not on line or section
        return False

    # Check for collisions of car with track borders
    def getCollisions(self, fr, fl, rr, rl):

        # Create list of above points in circle order (to take side sections in iterations)
        points = [fr, fl, rl, rr, fr]

        # For each car side chech collision with each track boundary section
        for side in zip(points, points[1:]):
            for section in zip(self.track, self.track[1:]):
                
                # Checking if car/track points are on track boundary/car side respectively (point on section)
                if self.pointOnSection(section[0], section[1], side[0]):
                    return True
                if self.pointOnSection(section[0], section[1], side[1]):
                    return True
                if self.pointOnSection(side[0], side[1], section[0]):
                    return True
                if self.pointOnSection(side[0], side[1], section[1]):
                    return True

                # Checking if sections are not crossing
                if (self.determinant(section[0], section[1], side[0]) * self.determinant(section[0], section[1], side[1])) >= 0:
                    pass
                elif (self.determinant(side[0], side[1], section[0]) * self.determinant(side[0], side[1], section[1])) >= 0:
                    pass
                else:  # Else sections are crossing
                    return True

        # No collisions detected
        return False
