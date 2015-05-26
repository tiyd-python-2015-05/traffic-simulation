import sys
import numpy as np

class Driver(object):

    def __init__(self, name = 'Sipho', max_speed = 30, acceleration = 2):
        self.name = name
        self.max_speed = max_speed      # in m/s
        self.accelaration = acceleration    #in m/s**2
        self.decelaration = deceleration    #in m/s**2


    def __str__(self):
        return "Driver {}".format(self.name)


    def stop(self):
        '''stops if they hit another car'''
        pass


class Road(object):

    def __init__(self, road_length = 1000, lanes = 1):
        '''Initialize a road with its length in meters, defaults to 0m'''
        self.road_length = road_length
        self.lanes = lanes


    def __str__(self):
        return "{}m-{}lane(s) Road".format(self.road_length, self.lanes)


    def __repr__(self):
        return ("Road:{}".format(self.road_length))


class Car(object):

    def __init__(self, max_speed = 33, current_speed = 1, car_number = 'J', length = 5, position = 5, acceleration = 2):
        self.length = length     # in meters
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.accelaration = acceleration    #in m/s**2
        self.car_number = car_number

    def __str__(self):
        return "Car {}".format(self.car_number)


    def ok_to_accelerate(self, distance_to_next_car):
        if distance_to_next_car > self.current_speed+self.acceleration and self.current_speed < self.max_speed:
            return True


    def accelerate(self, time=1):
        self.current_speed += int(self.acceleration * time)


    def decelerate(self, deceleration, time):
        self.current_speed -= int(deceleration * time)


class Simulator(object):

    def __init__(self, road, cars=None):
        if cars is None:
            cars = []
        self.cars = cars
        self.road = road
        self.car_locations = self.initial_car_locations()    # an array of car locations


    def initial_car_locations(self):
        return np.linspace(0, road.road_length, 30)


    def move(self):
        for car in self.cars:
            pass


if __name__ == '__main__':
    print("====Welcome to Traffic Simulator====")
    road = Road()
    sim = Simulator(road)
    print(sim.car_locations)
