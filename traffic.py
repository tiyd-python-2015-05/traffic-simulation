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
        self.top_speed = 33
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

    def decelerate(self):
        """
        Car decelerates at 2 meters/sec.
        """
        if self.speed > 0:
            self.speed = max(self.speed - self.decel, 0)

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

    def adjust_speed(self, other):
        if self.speed > other.speed:
            self.speed = other.speed
            #self.speed = other.position - self.position - self.length

        if self.position - self.length > other.position:
            self.stop()


class Road:
    def __init__(self, length = 1000):
        self.length = length


class Simulation:
    def __init__(self):
        self.cars = []
        self.car_positions = []
        self.car_speeds = []


    def put_cars_on_road(self):
        """
        Puts 30 cars on the road at equal distance
        """
        position = 0
        speed = 0
        for _ in range(30):
            position += 33
            car = Car(speed, position)
            self.cars.append(car)

    def run_simulation(self):
        self.put_cars_on_road()
        for i in range(60):
            self.run_cars()
            self.get_positions()
            self.get_speeds()


    def get_positions(self):
        positions = [car.position for car in self.cars]
        self.car_positions.append(positions)

    def get_speeds(self):
        speeds = [car.speed for car in self.cars]
        self.car_speeds.append(speeds)

    def run_cars(self):
        for car in self.cars:
            car.move_forward()
            car.get_position()
            car_location = self.cars.index(car)
            this_car = self.cars[car_location]
            car.adjust_speed(this_car)
