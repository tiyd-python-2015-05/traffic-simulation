import numpy as np
import random

class LeadCarException(Exception):
    pass


class Simulation:

    _delta = 1.0

    def __init__(self, cars, hard=False):
        if hard:
            self.track_length = 7000
        else:
            self.track_length = 1000
        if type(cars) is list:
            self.cars = cars
        elif type(cars) is int: # variable holds car density
            Ncars = cars * self.track_length // 1000
            positions = np.linspace(0, self.track_length, num=Ncars+1)
            car_list = [Car(positions[i]) for i in range(Ncars)]
            for i in range(Ncars-1):
                car_list[i].set_next(car_list[i+1])
            car_list[Ncars-1].set_next(car_list[0])
            self.cars = car_list
        for a_car in self.cars:
            a_car.speed = 0
            a_car.advance_time()
            if hard:
                a_car.hard = True
            a_car.track_length = self.track_length
        self.N = len(self.cars)
        self.time = 0


    def __str__(self):
        ret_st = " position: "
        for car in self.cars:
            ret_st += str(round(car.pos,2))+" "
        ret_st += "\n speed: "
        for car in self.cars:
            ret_st += str(round(car.speed,2))+" "
            '''
        ret_st += "\n leading: "
        for car in self.cars:
            ret_st += str(round(car.is_leader(),2))+" " '''
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
        # k = -1 # for implicit method
        # for i in range(n):
        #     if self.cars[i].is_leader():
        #         k = i
        #         break
        # if k == -1:
        #     raise LeadCarException
        for i in range(self.N):
#            j = self.index_fix(k - i)
            self.cars[i].move()
        for car in self.cars:
            car.advance_time()

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
        self.track_length = -1. # negative to signal should never use
        self.advance_time()
        self.hard = False

    def __str__(self):
        return "car at "+str(round(self._pos,2)).ljust(6) \
               +" going "+str(round(self.speed,2)).rjust(5)

    def advance_time(self):
        self.pos_old = self._pos
        self.speed_old = self.speed

    def set_next(self, other):
        self.next_car = other

    def move(self):
        '''Moves the car forward'''
        d = self.space()

        if random.random() < self.brake_chance(): # normal conditions
            self.speed -= 2
        elif self.speed < self.top_speed:
            self.speed += 2

        if d < 0: # limiter conditions
            self.speed = 0
        elif d < self.speed:
            self.speed = self.next_car.speed_old
        elif self.speed < 0:
            self.speed = 0
        elif self.speed > self.top_speed:
            self.speed = self.top_speed

        self._pos = (self._pos + self.speed) % self.track_length

    def is_leader(self):
        return self.space() > (self.speed + 2.0) * 2.0

    def brake_chance(self):
        if self.hard:
            if 1000 <= self._pos <= 2000:
                return 1.4*0.1
            elif 3000 <= self._pos <= 4000:
                return 0.2
            elif 5000 <= self._pos <= 6000:
                return 1.2*0.1
            else:
                return 0.1
        else:
            return 0.1

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
        next_pos = self.next_car.pos_old
        return (next_pos - self._pos) % self.track_length - self.length


if __name__ == '__main__':
    '''
    Ncars = 30 # was used for easy mode creation
    positions = np.linspace(0, 1000, num=Ncars+1)
    cars = [Car(positions[i]) for i in range(Ncars)]
    for i in range(Ncars-1):
        cars[i].set_next(cars[i+1])
    cars[Ncars-1].set_next(cars[0])
    print(cars[0])
    '''

    sim = Simulation(30, True)
    for i in range(300):
        sim.run_once()
#        print(sim.speed)
        print(str(round(np.mean(sim.speed_array()),2)), end=" ")
    print(" ")

    sim.run(60)
    print(" ")
    print(sim)

    print(sim.pos_array())
    print(" ")
    print(sim.speed_array())
