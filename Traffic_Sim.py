import random
import numpy as np

class Road:
    def __init__(self):
        self.start = 0
        self.end = 1000

class Car:
    def __init__(self, start_pos, road):
        self.position = start_pos
        self.speed = 0
        self.road = road

    def __repr__(self):
        return str(self.position)

    def check(self, front_car):
        dist = self.check_dist_to_front_car(front_car)
        if self.speed <= 0:
            self.accelerate()
        elif dist < self.speed:
            self.speed = dist
        else:
            if self.slow():
                if self.speed > 2:
                    self.speed -= 2
            else:
                if self.speed < 33.33:
                    self.accelerate()
        return (self.position, self.speed)

    def slow(self):
        s = random.random()
        if s < 0.1:
            return True
        else:
            return False

    def check_dist_to_front_car(self, front_car):
        if front_car.position < (self.position + self.speed):
            dist = ((self.road.end - (self.position + self.speed)) + front_car.position) - 5
        else:
            dist = (front_car.position - 5) - (self.position + self.speed)
        return dist

    def accelerate(self):
        self.speed += 2

    def set_new_position(self):
        self.position += self.speed
        if self.position > self.road.end:
            new_pos = self.position - self.road.end
            self.position = new_pos


class Simulation:
    def __init__(self, length):
        self.secs = length
        self.random_spots = np.linspace(0, 967, 30)[::-1]
        self.road = Road()
        self.cars = [Car(i, self.road) for i in self.random_spots]

    def start(self):
        the_results = []
        while self.secs > 0:
            one_sec = []
            for car in self.cars:
                idx = self.cars.index(car) - 1
                if idx == -1:
                    idx = 29
                pos_speed = car.check(self.cars[idx])
                one_sec.append(pos_speed)
                car.set_new_position()
            the_results.append(one_sec)
            self.secs -= 1
        return the_results


'''s = Simulation(120)
print(s.cars)
results = s.start()[60:]
print(results)'''