import random
import numpy as np

class Car:
    def __init__(self):
        # all distances in meters, all speeds in meters/second
        self.size = 5
        self.top_speed = 33.3
        self.acceleration = 2

    def accelerate(self, speed, accel_chance):
        if random.random() < 0.1 * accel_chance:
            if speed - 2 < 0:
                return 0
            else:
                return speed - 2
        else:
            if speed + self.acceleration <= self.top_speed:
                return speed + self.acceleration
            else:
                return self.top_speed

    def slow_down(self, distance, your_speed, their_speed, accel_chance=1):
        if distance <= your_speed:
            return their_speed
        else:
            return self.accelerate(your_speed, accel_chance)


class Aggressive(Car):
    def __init__(self):
        super().__init__()
        self.top_speed = 38.9
        self.acceleration = 5

    def accelerate(self, speed, accel_chance):
        if random.random() < 0.05 * accel_chance:
            if speed - 2 < 0:
                return 0
            else:
                return speed - 2
        else:
            if speed + self.acceleration <= self.top_speed:
                return speed + self.acceleration
            else:
                return self.top_speed


class Commercial(Car):
    def __init__(self):
        super().__init__()
        self.size = 25
        self.top_speed = 27.8
        self.acceleration = 1.5

    def slow_down(self, distance, your_speed, their_speed, accel_chance=1):
        if distance <= 2 * your_speed:
            return their_speed
        else:
            return self.accelerate(your_speed, accel_chance)


class Simulation:
    def __init__(self, road):
        self.road = road
        self.matrix = np.zeros((2, 120, 30))
