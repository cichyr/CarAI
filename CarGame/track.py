# Class representing track and collisions
class Track():

    # Initialize variables (track points)
    def __init__(self):
        self.trackOuterBoundary = [
            (960, 1080), 
            (960, 590),
            ]
        
        self.trackInnerBoundary = [
            (960, 1080), 
            (960, 590),
            ]
        
        # Cookies for AI - so it knows it does good job
        self.trackCookies = [
            (960, 1080), 
            (960, 590),
            ]
