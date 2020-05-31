# Class representing track and collisions
class Track():

    # Initialize variables (track points)
    def __init__(self):
        self.trackOuterBoundary = [
            (0, 404),
            (1920, 404)
        ]
        
        self.trackInnerBoundary = [
            (0, 510),
            (1920, 510)
        ]
        
        # Cookies for AI - so it knows it does good job
        self.trackCookies = [
            (200, 404),
            (200, 510),
            (400, 404),
            (400, 510),
            (600, 404),
            (600, 510),
            (800, 404),
            (800, 510),
            (1000, 404),
            (1000, 510),
            (1200, 404),
            (1200, 510),
            (1400, 404),
            (1400, 510),
            (1600, 404),
            (1600, 510),
            (1800, 404),
            (1800, 510)
        ]

        self.track_finish = [
            (1900, 404),
            (1900, 510)
        ]


# Example of trackBoundary
#self.trackOuterBoundary = [
#    (960, 1080), 
#    (960, 590),
#]