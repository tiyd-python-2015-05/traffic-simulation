__author__ = 'joshuahiggins'

class Car:
    def __init__(self, speed=0):
        """Car has length 5 and speed 0 to start.  Can pass speed."""
        self.length = 5
        self.speed = speed


    def accelerate(self):
        """When car accelerates, goes 2m/s faster next time."""
        self.speed += 2


    def decelerate(self):
        """When car decelerates, goes 2m/s slower next time."""
        self.speed -= 2


    def slow_down(self, other):
        """Car sets itself to other car's speed."""
        self.speed = other.speed






