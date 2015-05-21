
"""
Responsibilities:
  Car:
    Must know about car in front's current position and speed
    Created with an accel rate, desired speed, size, min spacing,
      slowing chance, length (assume 5m for now)
    At each time step, make decision whether to speed up, slow down, or stop,
      based on leading car's current position/speed, self's desired following distance,
      and self's current speed, desired speed, and slowing chance, and road conditions
    Car stops if continuing will cause a collision (collisions not modeled)
    Ask the Road current road condition
    Ask the Road if current position is valid or has to turn over
"""


class Car():
    def __init__(self, desired_speed=120, length=5, accel_rate=2,
                slowing_chance=0.1, decel_rate=2, init_speed=60,
                desired_spacing_factor=1):
        self.desired_speed = desired_speed
        self.length = length
        self.accel_rate = accel_rate
        self.slowing_chance = slowing_chance
        self.decel_rate = decel_rate
        self.speed = init_speed
        self.desired_spacing_factor = desired_spacing_factor

    @property
    def desired_spacing(self):
        return self.speed * self.desired_spacing_factor
