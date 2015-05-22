import random
import numpy as np
from collections import deque


class Simulator:
    def __init__(self, cars, road, delta):
        self.cars = deque(cars, maxlen=len(cars))

        for car in self.cars:
            car.index = cars.index(car)
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
    def next(self):
        self._next = self._loc + self._speeds * self.delta
        for car in self.cars:
            car.next = self._next[car.index]

        return self._next

    def speed_change(self):
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
        speed to match car ahead, then rechecks.
        """

        n= sum(1 for item in self.next if item > self.road.length)
        self.cars.rotate(n)
        again = False

        for car in self.cars:
            if not car.safe:
                    self._speeds[car.index] = self._speeds[car.next_car.index]
                    again = True


    def tell(self):
        for car in self.cars:
            car.loc = self._loc[car.index]
            car.current_speed = self._speeds[car.index]

    def update(self):
        self.history.append(self._loc)
        self.speed_history.append(self._speeds)
        self._loc = self.next % self.road.length
        self.tell()

    def step(self):
        self.speed_change()
        self.check_next()
        self.update()


    def loop(self, n):
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

    def reset(self):
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

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, other):
        self._next = other

    @property
    def safe(self):
        """
        returns True if the next calculated location
        is safe
        """
        return self.next_car.next > self.next + self.length * self.min_mult \
               + self.current_speed




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
