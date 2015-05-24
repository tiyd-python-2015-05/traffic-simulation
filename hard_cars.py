__author__ = 'joshuahiggins'
import random

class Car:
    def __init__(self, speed=0):
        """Car has length 5 and speed 0 to start.  Can pass speed."""
        self.length = 5
        self.speed = speed
        self.location = 0
        self.decelerate_chance = 1
        #self.accelerate_chance will be changed by the simulation for longer distances


    def accelerate(self):
        """When car accelerates, goes 2m/s faster next time."""
        self.speed += 2
        if self.speed > 34:
            self.speed = 34


    def decelerate(self):
        """When car decelerates, goes 2m/s slower next time."""
        self.speed -= 2
        if self.speed < 0:
            self.speed = 0


    def slow_down(self, other):
        """Car sets itself to other car's speed."""
        #self.speed = (((other.location - 5) - self.location))
        #correct if other car just lapped 1000
        if ((other.location - 5) - self.location) < 0:
            if (((other.location + 995) - self.location) - 2) < 0:
                self.speed = 0
            else:
                self.speed = (((other.location + 995) - self.location) - 2)
        else:
            if (((other.location - 5) - self.location) - 2) < 0:
                self.speed = 0
            else:
                self.speed = (((other.location - 5) - self.location) - 2)



    def calculate_slowdown(self, other):
        """Returns true if car distance to next car is less than speed"""
        #Need to work out location when it loops back
        if ((other.location - 5) - self.location ) < 0:
            if other.location + 995 - self.location < self.speed:
                return True
            else:
                return False
        elif ((other.location - 5) - self.location) < self.speed + 3:
            return True
        else:
            return False

    def set_decelerate_chance(self):
        """This should be for hard mode"""
        pass

    def set_speed(self, other):
        """Sets car speed based on self.location and other.location"""
        if self.calculate_slowdown(other):
            self.slow_down(other)
        else:
            if random.random() <= (.1 * self.decelerate_chance):
                self.decelerate()
            else:
                self.accelerate()









