import random
import numpy as np
import statistics as st


class Car:
    """
    Creates a car at the beginning of the Road.
    Initial speed is zero, but can go as fast as
    33.33 meters/sec.
    """
    def __init__(self, speed = 0, position = 0):
        self.length = 5
        self.speed = speed
        self.top_speed = 33.33
        self.position = position
        self.accel = 2
        self.decel = 2

    def accelerate(self):
        """
        Car accelerates at 2 meters/sec if speed is less
        than top speed.
        """
        if self.speed < self.top_speed:
            self.speed = min(self.speed + self.accel, self.top_speed)
            self.position += self.speed

    def decelerate(self):
        """
        Car decelerates at 2 meters/sec.
        """
        if self.speed > 0:
            self.speed = max(self.speed - self.decel, 0)
            self.position  -= self.speed

    def stop(self):
        """
        Stops the car if it is going to collide.
        """
        self.speed = 0

    def get_position(self):
        self.position = (self.position + self.speed) % 1000

    def move_forward(self):
        if random.random() <= 0.1:
            self.decelerate()
        else:
            self.accelerate()


class Road:
    def __init__(self, length = 1000):
        self.length = length



class Simulation:
    def __init__(self, cars = 30):
        self.cars = cars

    



if __name__ == "__main__":
    bug = Car()
