import random
class Car:

    def __init__(self, speed=0):
        self.size = 5
        self.speed = speed
        self.location = 0
        self.decelerate_chance = 1

    def accelerate(self):
        """Can increase until speed reaches highest speed of 34m/s"""
        self.speed += 2
        if self.speed > 34:
            self.speed = 34

    def decelerate(self):
        """If current speed is 0 the decelerate will not be less than 0."""
        self.speed -= 2
        if self.speed < 0:
            self.speed = 0

    def slow_down(self, other):
        """Make the self.speed the same speed as car in front"""
        # self.speed = other.speed  <- can't do this beacause you get tailgaters that never leave
        if ((other.location - 5) - self.location) < 0:
            if (((other.location + 6995) - self.location) - 2) < 0:
                self.speed = 0
            else:
                self.speed = (((other.location + 6995) - self.location) - 2)

        else:
            if (((other.location - 5) - self.location) - 2) < 0:
                self.speed = 0
            else:
                self.speed = (((other.location - 5) - self.location) - 2)

    def calculate_slow_down(self, other):
        """Returns true if other car distance is less than speed of current car."""
        # if other location is is greater than 1000 needs to know what to do
        if ((other.location - 5) - self.location) < 0:
            if other.location + 6995 - self.location < self.speed + 3:
                return True
            else:
                return False
        elif ((other.location - 5) - self.location) < self.speed + 3:
            return True
        else:
            return False

    def set_decelerate_chance(self):
        """For hard mode. Changes based on road curve."""
        if 0 < self.location <= 1000:
            self.decelerate_chance = 1
        elif 1001 < self.location <= 2000:
            self.decelerate_chance = 1.4
        elif 2001 <self.location <= 3000:
            self.decelerate_chance = 1
        elif 3001 <self.location <= 4000:
            self.decelerate_chance = 2
        elif 4001 <self.location <= 5000:
            self.decelerate_chance = 1
        elif 5001 <self.location <= 6000:
            self.decelerate_chance = 1.2
        elif 6001 <self.location <= 7000:
            self.decelerate_chance = 1

    def set_speed(self, other):
        """Sets car speed based on self.location and other.location"""
        if self.calculate_slow_down(other):
            self.slow_down(other)
        else:
            self.set_decelerate_chance()
            if random.random() <= (.1 * self.decelerate_chance):
                self.decelerate()
            else:
                self.accelerate()
