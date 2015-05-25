import random
import numpy as np

class Car:
    def __init__(self):
        # all distances in meters, all speeds in meters/second
        self.size = 5
        self.top_speed = 33.3
        self.acceleration = 2

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def accelerate(self, speed, accel_chance):
        if random.random() < (0.1 * accel_chance):
            if speed - 2 < 0:
                return 0
            else:
                return speed - 2
        else:
            if speed + self.acceleration <= self.top_speed:
                return speed + self.acceleration
            else:
                return self.top_speed

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def set_speed(self, distance, your_speed, accel_chance=1):
        new_speed = self.accelerate(your_speed, accel_chance)
        if distance <= new_speed:
            return distance
        else:
            return new_speed


#######################################################################################################################
#######################################################################################################################


class Aggressive(Car):
    def __init__(self):
        super().__init__()
        self.top_speed = 38.9
        self.acceleration = 5

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def accelerate(self, speed, accel_chance):
        if random.random() < (0.05 * accel_chance):
            if speed - 2 < 0:
                return 0
            else:
                return speed - 2
        else:
            if speed + self.acceleration <= self.top_speed:
                return speed + self.acceleration
            else:
                return self.top_speed


#######################################################################################################################
#######################################################################################################################


class Commercial(Car):
    def __init__(self):
        super().__init__()
        self.size = 25
        self.top_speed = 27.8
        self.acceleration = 1.5

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def set_speed(self, distance, your_speed, accel_chance=1):
        new_speed = self.accelerate(your_speed, accel_chance)
        if distance <= 2 * new_speed:
            return distance
        else:
            return new_speed


#######################################################################################################################
#######################################################################################################################


class Simulation:
    def __init__(self, cars, road, n=122):
        self.cars = cars
        self.road = road
        self.values = np.zeros((2, n, len(self.cars)))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def initial_positions(self):
        self.values[0][0] = np.linspace(5, (self.road-5), len(self.cars))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def initial_speeds(self):
        self.values[1][0] = np.zeros(len(self.cars))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def find_distance(self, time, car, other_car):
        rear_bumper = self.values[0][time-1][other_car] - self.cars[other_car].size
        distance = rear_bumper - self.values[0][time-1][car]
        if distance < 0:
            distance += self.road
        return distance

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def get_speed(self, distance, time, car):
        position = self.values[0][time-1][car]
        your_speed = self.values[1][time-1][car]
        if position <= 1000:
            return self.cars[car].set_speed(distance, your_speed)
        elif 1000 < position <= 2000:
            return self.cars[car].set_speed(distance, your_speed, accel_chance=1.4)
        elif 2000 < position <= 3000:
            return self.cars[car].set_speed(distance, your_speed)
        elif 3000 < position <= 4000:
            return self.cars[car].set_speed(distance, your_speed, accel_chance=2.0)
        elif 4000 < position <= 5000:
            return self.cars[car].set_speed(distance, your_speed)
        elif 5000 < position <= 6000:
            return self.cars[car].set_speed(distance, your_speed, accel_chance=1.2)
        elif 6000 < position <= 7000:
            return self.cars[car].set_speed(distance, your_speed)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    def run_simulation(self):
        self.initial_positions()
        self.initial_speeds()
        for time in range(1, (len(self.values[0]))):
            for car in range(len(self.values[0][time])):
                if car < (len(self.cars) - 1):
                    other_car = car + 1
                else:
                    other_car = 0

                distance = self.find_distance(time, car, other_car)
                self.values[1][time][car] = self.get_speed(distance, time, car)
            self.values[0][time] = self.values[0][time-1] + self.values[1][time]
            for index in range(len(self.values[0][time])):
                if self.values[0][time][index] > self.road:
                    self.values[0][time][index] -= self.road
        return self.values[:, 61:, :]


#######################################################################################################################
#######################################################################################################################


def create_cars(number, one_type=True):
    if one_type:
        car_list = [Car() for _ in range(number)]
    else:
        car_list = []
        for n in range(number):
            choice = random.random()
            if choice <= 0.1:
                car_list.append(Aggressive())
            elif 0.1 < choice <= 0.25:
                car_list.append(Commercial())
            else:
                car_list.append(Car())
    return car_list