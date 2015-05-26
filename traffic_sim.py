import numpy as np
import statistics



class Car:
    def __init__(self, speed=0):
        self.size = 5
        self.maximum_speed = 33.33
        self.chance = .10
        self.acceleration = 2
        self.speed = speed

    def accelerate(self):
        if self.speed < self.maximum_speed:
            self.speed += self.acceleration
            return self.speed

    def decelerate(self):
        self.speed -= self.acceleration
        return self.speed


# class Simulation:
    # def __init__(self,length=1000, number_of_cars=30):
        # pass
