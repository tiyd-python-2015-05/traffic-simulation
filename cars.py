import random
import numpy as np
from collections import deque

class Simulator:
    def __init__(self, cars, road, delta):
        self.cars = deque(cars)

        for car in self.cars:
            car.index = cars.index(car)
            car.road_length = road.length

            if car.index == len(self.cars) - 1:
                car.next_car = self.cars[0]
            else:
                car.next_car = self.cars[car.index + 1]


        self.road = road
        self.delta = delta
        self.length = len(self.cars)

        self._loc = np.linspace(0, road.length, len(cars), endpoint=False)
        self._speeds = np.zeros(len(self.cars))
        self._next = np.zeros(len(self.cars))
        self.history = []
        self.speed_history = []

    @property
    def next_pos(self):
        """
        the next location of each car
        """
        self._next = self._loc + self._speeds * self.delta
        for car in self.cars:
            car.next_pos = self._next[car.index]

        return self._next

    def speed_change(self):
        """
        calculates the next speed for each car
        """
        for car in self.cars:
            seg = self.road.segment(car.loc)

            if car.current_speed == 0:
                self._speeds[car.index] += car.inc

            elif car.current_speed < car.target_speed:
                if random.random() <= seg * car.chance:
                    self._speeds[car.index] -= car.inc
                else:
                    self._speeds[car.index] += car.inc
            else:
                if random.random() <= seg * car.chance:
                    self._speeds[car.index] -= car.inc


    def check_next(self):
        """
        checks next position
        for collision with safe zone and changes
        speed to match car ahead if there
        would have been one
        """
        self.next_pos

        for car in self.cars:
            if not car.safe:
                    self._speeds[car.index] = self._speeds[car.next_car.index]



    def tell(self):
        """
        updates the car's information
        """
        for car in self.cars:
            car.loc = self._loc[car.index]
            car.current_speed = self._speeds[car.index]

    def update(self):
        """
        pushes the locations and speeds into the history
        and updates the locations,
        then tells the cars what they did
        """
        self.history.append(self._loc)
        self.speed_history.append(self._speeds)
        
        next_pos = self.next_pos
        
        for idx in range(self.length):
            if next_pos[idx] > self._loc[idx]:
                self.cars.rotate(1) # for checking the car order
        
        self._loc = next_pos % self.road.length
        self.tell()

    def step(self):
        """
        one step forward
        """
        self.speed_change()
        self.check_next()
        self.update()


    def loop(self, n):
        """
        calculates n steps forward
        returns the history of those
        steps
        """
        m = 60
        while m:
            self.speed_change()
            self.check_next()
            self.update()

            m -= 1

        self.history = []
        self.speed_history = []
        while n:
            self.speed_change()
            self.check_next()
            self.update()
            n -= 1

        return np.array(self.history), np.array(self.speed_history)
    
    def errors(self):
        for car in self.cars:
            if not car._loc < car.next._loc:
                raise Exception("Cars out of order!")
    
    def reset(self):
        """
        flushes the history
        resets to original locations
        and zero speeds
        """
        self._loc = self.history[0]
        self.history = []
        self.speeds = np.zeros(len(self.cars))
        self._next = np.zeros(len(self.cars))


class Car:
    def __init__(self, target_speed=34, length=5, inc=2, min_mult=1, chance=.1):
        self.loc = 0
        self.target_speed = target_speed
        self.length = length
        self.inc = inc
        self._front = self.length + self.loc
        self.current_speed = 0
        self.index = 0
        self._next = 0
        self.next_car = self
        self.min_mult = min_mult
        self.chance=chance
        self.road_length = 1

    @property
    def next_pos(self):
        return self._next

    @next_pos.setter
    def next_pos(self, other):
        self._next = other

    @property
    def safe(self):
        """
        returns True if the next calculated location
        is safe
        """
        # no wrapping
        first = self.next_car.next_pos > self.front_zone and \
                self.next_car.next_pos % self.road_length > self.next_car.loc

        # car ahead wraps, safe zone wraps
        second = self.next_car.next_pos % self.road_length < self.next_car.loc and \
                 self.front_zone % self.road_length < self.loc and \
                 self.next_car.next_pos % self.road_length < self.front_zone \
                % self.road_length

        # car ahead wraps, safe zone doesn't
        third = self.next_car.next_pos % self.road_length < self.next_car.loc and \
                 self.front_zone % self.road_length > self.loc

        if first or second or third:
            return True
        return False

    @property
    def front_zone(self):
        return self.next_pos + self.length * self.min_mult + self.current_speed


class Road:
    """
    in 1km segments
    """
    def __init__(self, length=1, mods=[1]):
        if len(mods) != length:
            raise KeyError("Length and number of modifiers must match")

        self.length = length*1000
        self.mods = mods

    def segment(self, location):
        return self.mods[int(location/1000)] # assumes 1km segments
