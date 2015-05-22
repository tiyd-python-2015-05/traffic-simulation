import numpy as np
import random

class LeadCarException(Exception):
    pass


class Simulation:

    _delta = 1.0

    def __init__(self, cars):
        self.cars = cars
        self.N = len(self.cars)
        self.time = 0

    def __str__(self):
        ret_st = " position: "
        for car in self.cars:
            ret_st += str(round(car.pos,2))+" "
        ret_st += "\n speed: "
        for car in self.cars:
            ret_st += str(round(car.speed,2))+" "
        ret_st += "\n leading: "
        for car in self.cars:
            ret_st += str(round(car.is_leader(),2))+" "
        return ret_st


    def dist_array(self):
        ret_array = np.empty(self.N)
        for i in range(self.N):
            ret_array[i] = self.cars[i].space()
        return ret_array

    def pos_array(self):
        ret_array = np.empty(self.N)
        for i in range(self.N):
            ret_array[i] = self.cars[i].pos
        return ret_array

    def speed_array(self):
        ret_array = np.empty(self.N)
        for i in range(self.N):
            ret_array[i] = self.cars[i].speed
        return ret_array


    def run_once(self):
        n = len(self.cars)
        k = -1
        for i in range(n):
            if self.cars[i].is_leader():
                k = i
                break
        if k == -1:
            raise LeadCarException
        for i in range(self.N):
            j = self.index_fix(k - i)
            self.cars[j].move()

    def index_fix(self, i):
        if i < 0:
            return self.N + i
        elif i >= self.N:
            return i - self.N
        else:
            return i


    def run(self, end_time):
        while self.time <= end_time:
            self.run_once()
            self.time += self._delta

    @property
    def delta(self): return self._delta
    @delta.setter
    def delta(self, x): self._delta = x


class Car:

    _pos = 0
    _length = 0

    def __init__(self, position):
        self._length = 5
        self._pos = position
        self.top_speed = 33.333
        self.speed = 0
        self.acc = 0
        self.track_length = 1000.

    def __str__(self):
        return "car at "+str(round(self._pos,2)).ljust(6) \
               +" going "+str(round(self.speed,2)).rjust(5)

    def set_next(self, other):
        self.next_car = other

    def move(self):
        '''Moves the car forward'''
        d = self.space()

        if random.random() < 0.1: # normal conditions
            self.speed -= 2
        elif self.speed < self.top_speed:
            self.speed += 2

        if d < 0: # limiter conditoins
            self.speed = 0
        elif d < self.speed:
            self.speed = self.next_car.speed
        elif self.speed < 0:
            self.speed = 0
        elif self.speed > self.top_speed:
            self.speed = self.top_speed

        self._pos = (self._pos + self.speed) % 1000

    def is_leader(self):
        return self.space() > (self.speed + 2.0) * 2.0

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, x):
        self._pos = x

    @property
    def length(self):
        return self._length
    @length.setter
    def length(self, x):
        self._length = x

    def space(self):
        next_pos = self.next_car._pos
        return (next_pos - self._pos) % 1000 - self.length


if __name__ == '__main__':
    Ncars = 30
    positions = np.linspace(0, 1000, num=Ncars+1)
    cars = [Car(positions[i]) for i in range(Ncars)]
    for i in range(Ncars-1):
        cars[i].set_next(cars[i+1])
    cars[Ncars-1].set_next(cars[0])
    print(cars[0])
    print(cars[0].space())
    print(cars[Ncars-1].space())
    print(1010%1000)

    sim = Simulation(cars)
    for i in range(30):
        sim.run_once()
#        print(sim.speed)
        print(np.mean(sim.speed_array()))

    sim.run(60)
    print(" ")
    print(sim)
    print([int(car.space()*10)/10 for car in cars])
#    print([car.pos for car in cars])
#    print([car.is_leader() for car in cars])

    print(sim.pos_array())
    print(" ")
    print(sim.speed_array())
