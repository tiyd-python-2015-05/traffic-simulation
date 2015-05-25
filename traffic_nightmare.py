import random
import numpy as np

class PassException(Exception):
    pass

class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Car:
    def __init__(self, start_pos, road, max_speed = 33.33, accel = 2.0, size = 5, min_spc = 1.0, slw_chce = 1.0):
        self.position = start_pos
        self.speed = 0
        self.road = road
        self.lead_car = False
        self.old_position = start_pos
        self.slow_down = False
        self.max_speed = max_speed
        self.accel = accel
        self.size = size
        self.min_spc = min_spc
        self.slw_chance = slw_chce

    def __repr__(self):
        return str(self.position)

    def check(self, front_car):
        dist = self.check_dist_to_front_car(front_car)
        if self.speed == 0 and dist > 2:
            self.accelerate()
        elif dist < (self.speed * self.min_spc):
            self.speed = (dist)
        elif dist <= 0:
            self.speed = 0
        else:
            if self.slow() and self.speed > 2:
                self.speed -= 2
            elif self.speed < self.max_speed:
                self.accelerate()
        if self.test_new_position() >= (front_car.position - front_car.size):
            if not front_car.lead_car:
                self.speed = 0
        self.old_position = self.position
        self.set_new_position(front_car)
        return (self.position, self.speed)

    def test_new_position(self):
        return self.position + self.speed

    def slow(self):
        slow = random.random()
        if 1000 < self.position < 2000:
            if slow < (0.14 * self.slw_chance):
                return True
            else:
                return False
        elif 3000 < self.position < 4000:
            if slow < (0.2 * self.slw_chance):
                return True
            else:
                return False
        elif 5000 < self.position < 6000:
            if slow < (0.12 * self.slw_chance):
                return True
            else:
                return False
        else:
            if slow < (0.1 * self.slw_chance):
                return True
            else:
                return False

    def check_dist_to_front_car(self, front_car):
        if front_car.old_position < self.position:
            dist = ((self.road.end - self.position) + front_car.old_position) - front_car.size
        else:
            dist = (front_car.old_position - front_car.size) - self.position
        return dist

    def accelerate(self):
        self.speed += self.accel

    def set_new_position(self, front_car):
        self.position += self.speed
        if self.position > self.road.end:
            new_pos = self.position - self.road.end
            self.position = new_pos
            self.lead_car = True
            front_car.lead_car = False


class Simulation:
    def __init__(self, length, rd_length, nightmare = False):
        self.secs = length
        if rd_length == 1000:
            self.road = Road(0, 1000)
            self.random_spots = np.linspace(0, self.road.end, 30, endpoint=False)[::-1]
            self.cars = [Car(i, self.road) for i in self.random_spots]
        else:
            self.road = Road(0, 7000)
            self.random_spots = np.linspace(0, self.road.end, 210, endpoint=False)[::-1]
            if nightmare:
                self.cars = [self.pick_car(i, self.road) for i in self.random_spots]
            else:
                self.cars = [Car(i, self.road) for i in self.random_spots]
        self.cars[len(self.cars) - 1].lead_car = True

    def pick_car(self, i, road):
        r = random.random()
        if r < 0.1:
            car = Car(i, road, max_speed = 38.88, accel = 5, size = 5, min_spc = 1, slw_chce = 0.5)
        elif 0.1 <= r < .25:
            car = Car(i, road, max_speed = 27.77, accel = 1.5, size = 25, min_spc = 2, slw_chce = 1)
        else:
            car = Car(i, road)
        return car

    def check_for_passes(self):
        for car in self.cars:
            front_car = self.cars[self.cars.index(car)-1]
            if front_car.position < car.position:
                if not front_car.lead_car:
                    print(self.cars.index(car))
                    print(car.position)
                    print(front_car.position)
                    raise PassException()

    def start(self):
        the_results = []
        while self.secs > 0:
            one_sec = []
            for car in self.cars:
                idx = self.cars.index(car) - 1
                if idx == -1:
                    idx = len(self.cars) - 1
                pos_speed = car.check(self.cars[idx])
                one_sec.append(pos_speed)
            the_results.append(one_sec)
            self.check_for_passes()
            self.secs -= 1
        return the_results


'''s = Simulation(1000, 7000, nightmare=True)
results = s.start()[995:]
print(results)'''