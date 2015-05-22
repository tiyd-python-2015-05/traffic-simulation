import random
import road
from itertools import cycle

"""
Responsibilities:
  Car:
    Must know about car in front's current position and speed
    Created with an accel rate, desired speed, size, min spacing,
      slowing chance, length (assume 5m for now), position
    At each time step, make decision whether to speed up, slow down, or stop,
      based on leading car's current position/speed, self's desired following distance,
      and self's current speed, desired speed, and slowing chance, and road conditions
      THEN update position with new speed, etc
    Car stops if continuing will cause a collision (collisions not modeled)
    Ask the Road current road condition
    Ask the Road if current position is valid or has to turn over
"""

class Car():
    def __init__(self, road, position=0, desired_speed=120, length=5, accel_rate=2,
                slowing_chance=0.1, decel_rate=2, init_speed=60,
                desired_spacing_factor=1, s_per_step=1):
        self.road = road
        self.desired_speed = desired_speed
        self.length = length
        self.accel_rate = accel_rate
        self.slowing_chance = slowing_chance
        self.decel_rate = decel_rate
        self.speed = init_speed
        self.desired_spacing_factor = desired_spacing_factor
        self.position = road.validate(position)
        self.s_per_step = s_per_step

    @property
    def desired_spacing(self):
        return self.speed * self.desired_spacing_factor

    @property
    def m_per_s(self):
        kmh_to_mps = 1000 / 3600  # (1000m/km) / (60s * 60m)
        return self.speed * kmh_to_mps

    def accelerate(self):
        self.speed = self.speed + self.accel_rate
        if self.speed > self.desired_speed:
            self.speed = self.desired_speed

    def stop(self):
        self.speed = 0

    def update_position(self):
        self.position = self.road.validate(self.position +
                                           self.m_per_s * self.s_per_step)
        return self.position

    def match_speed(self, car2):
        self.speed = car2.speed if car2.speed < self.speed else self.speed

    def decelerate(self):
        self.speed = self.speed - self.decel_rate * self.s_per_step
        if self.speed < 0:
            self.speed = 0

    def brake_if_needed(self, car2):
        rear_bumper = self.road.validate(car2.position - car2.length)
        buffer_zone = self.road.validate(rear_bumper - self.desired_spacing)
        potential_position = self.road.validate(self.position + self.m_per_s *
                                                self.s_per_step)
        print('rear_bumper: {}, buffer_zone: {}, potential_position: {}'.format(
              rear_bumper, buffer_zone, potential_position))
        if self.speed > self.desired_speed:
            self.speed = self.desired_speed

        if potential_position >= rear_bumper:
            self.stop()
            return True
        elif potential_position >= buffer_zone:
            self.match_speed(car2)
            return True
        elif random.random() < self.slowing_chance:
            self.decelerate()
            return True
        else:
            return False

    def step(self, car2):
        did_brake = self.brake_if_needed(car2)
        if not did_brake:
            self.accelerate()
        self.update_position()
        return self.position, self.speed
