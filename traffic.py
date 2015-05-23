import numpy as np
import random
import statistics as st
import math

class LeadCarException(Exception):
    pass

class BuildError(Exception):
    pass


class Simulation:

    _delta = 1.0

    def __init__(self, cars, hard=False, nightmare=False):
        if hard:
            self.track_length = 7000
        else:
            self.track_length = 1000
        if type(cars) is list:
            self.cars = cars
        elif type(cars) is int: # variable holds car density
            Ncars = cars * self.track_length // 1000
            positions = np.linspace(0, self.track_length, num=Ncars+1)
            if nightmare:
                slots = [i for i in range(Ncars)]
                ct_cars = int(0.75*Ncars)
                ct_crazy = int(0.1*Ncars)
                ct_truck = Ncars - ct_cars - ct_crazy
                car_list = [0 for i in range(Ncars)]
                for i in range(ct_cars):
                    k = random.choice(slots)
                    car_list[k] = Car(positions[k], type=1)
                    slots.remove(k)

                for i in range(ct_crazy):
                    k = random.choice(slots)
                    car_list[k] = Car(positions[k], type=2)
                    slots.remove(k)

                for i in range(ct_truck):
                    k = random.choice(slots)
                    car_list[k] = Car(positions[k], type=3)
                    slots.remove(k)
                for i in car_list:
                    if type(i) is int:
                        print(car_list)
                        raise BuildError
            else:
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

    def dist_list(self):
        return [self.cars[i].space() for i in range(self.N)]

    def pos_list(self):
        return [self.cars[i]._pos for i in range(self.N)]

    def speed_list(self):
        return [self.cars[i].speed for i in range(self.N)]

    def suggest_speed(self):
        self.time = 0
        speeds = []
        for i in range(60):
            self.run_once()
        Nruns = 1000
        for i in range(Nruns):
            for k in range(5):
                self.run_once()
            speeds.append(self.speed_array()[0].tolist())
        std = st.stdev(speeds)
        mean = st.mean(speeds)
        ret_st = " mean= "+str(round(std,4)) + " \n"
        ret_st += " stdev= "+str(round(mean,4)) + "\n"
        ret_st += "  suggested speed= "+str(round(std+mean,4))+" m/s \n"
        ret_st += "                 = "
        ret_st += str(round((std+mean)*3.6,4))+" km/h "
        ret_st += " with expected variation: "
        ret_st += str(round(std/math.sqrt(Nruns),4))+" \n"
        ret_st += "                 = "
        ret_st += str(int((std+mean)*3.6))+" km/h \n"
        return ret_st


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


    def run(self, time_int):
        end_time = self.time + time_int
        while self.time <= end_time:
            self.run_once()
            self.time += self._delta

    def produce_history(self, Ntime):
        avg_speed = [0] * Ntime
        full_hist = [[0 for i in range(self.N)] for j in range(Ntime)]
        for i in range(Ntime):
            avg_speed[i] = self.speed_array().mean()
            full_hist[i] = self.pos_list()
            self.run_once()
        return avg_speed, full_hist

    @property
    def delta(self): return self._delta
    @delta.setter
    def delta(self, x): self._delta = x


class Car:

    _pos = 0
    _length = 0

    def __init__(self, position, type=1):
        if type == 1:
            self.acc = 2
            self.top_speed = 33.333
            self._length = 5
            self.spacing_factor = 1
            self.bsc = 0.1 # base slowing chance
        elif type == 2:
            self.acc = 5
            self.top_speed = 38.888
            self._length = 5
            self.spacing_factor = 1
            self.bsc = 0.05
        elif type == 3:
            self.acc = 1.5
            self.top_speed = 27.777
            self._length = 25
            self.spacing_factor = 2
            self.bsc = 0.15

        self._pos = position
        self.speed = 0
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
            self.speed += self.acc

        if d < self.speed * self.spacing_factor:
            #self.speed = self.next_car.speed_old
            self.speed = d
        elif self.speed < 0:
            self.speed = 0
        elif self.speed > self.top_speed:
            self.speed = self.top_speed

        d = self.space()
        if d < 0:
            self.speed = 0

        self._pos = (self._pos + self.speed) % self.track_length

    def is_leader(self):
        return self.space() > (self.speed + 2.0) * 2.0

    def brake_chance(self):
        if self.hard:
            if 1000 <= self._pos <= 2000:
                return 1.4*self.bsc
            elif 3000 <= self._pos <= 4000:
                return 2.0*self.bsc
            elif 5000 <= self._pos <= 6000:
                return 1.2*self.bsc
            else:
                return self.bsc
        else:
            return self.bsc

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

    sim = Simulation(30, False, False)
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
    print(sim.speed_array().tolist()[0])

    print(sim.suggest_speed())
    print(" ")

    sim = Simulation(30, False, False)
    speeds, hist = sim.produce_history(2000)

    print(" Speed graph:")
    for i in range(20):
        print("#" * int(speeds[i]))

    print(" ")
    print(hist[0])
