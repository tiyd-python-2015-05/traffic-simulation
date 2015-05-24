import random
import road
from itertools import cycle, count


"""
Responsibilities:
  Car:
    Must know about car in front's current position Xand speedX
    Created with an accel rate, desired speed, size, min spacing,
      slowing chance, length (assume 5m for now), position
    At each time step, make decision whether to speed up, slow down, X or stop,X
      based on leading car's current positionX/speedX, self's desired following
      distance, and self's current speed, desired speed,
      and slowing chance, and road conditions
      THEN update position with new speed, etc
    XCar stops if continuing will cause a collision (collisions not modeled)X
    Ask the Road current road condition
    Ask the Road if current position is valid or has to turn over
"""

class TeleportationError(Exception):
    pass

class Car():
    """Car class for traffic simulation. Units of m and m/s"""
    _ids = count(0)

    def __init__(self, road, position=0, desired_speed=33.333, length=5, accel_rate=2,
                slowing_chance=0.1, decel_rate=2, init_speed=15,
                desired_spacing_factor=1, s_per_step=1):
        self.id = next(self._ids)
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

    def __repr__(self):
        return 'id:{} x:{} s:{}'.format(self.id, round(self.position,2),
                                        round(self.speed, 2))

    def accelerate(self):
        self.speed = self.speed + self.accel_rate
        if self.speed > self.desired_speed:
            self.speed = self.desired_speed

    def stop(self):
        self.speed = 0
        print('id#{} Stopping'.format(self.id))

    def update_position(self, car2):
        leading_car = self.road.validate(car2.position)
        potential_position = self.potential_position()
        if potential_position > leading_car \
            and self.road.validate(self.position) < leading_car:
            raise TeleportationError("{} is attempting to pass through {}."
                                     .format(self, car2))
        self.position = potential_position
        return self.position

    def decelerate(self):
        self.speed = self.speed - self.decel_rate * self.s_per_step
        if self.speed < 0:
            self.speed = 0
        print('id#{} Slowing'.format(self.id))

    def potential_position(self):
        return self.road.validate(self.position + self.speed *
                                  self.s_per_step)

    def distance_behind(self, leading_car):
        # TODO: Add tests
        self.position = self.road.validate(self.position)
        leading_car.position = self.road.validate(leading_car.position)
        # Both cars must have same road

        if leading_car.position < self.position:
            return leading_car.position - leading_car.length - self.position \
                + self.road.length
        else:
            return leading_car.position - leading_car.length - self.position

    def brake_if_needed(self, leading_car):
        if self.speed > self.desired_speed:
            self.speed = self.desired_speed

        braked = False

        # Avoid leapfrogging
        lead_distance = self.distance_behind(leading_car)
        if self.speed > lead_distance:
            self.speed = lead_distance
            print("Braking")
            braked = True

        print('id#{} lead_distance {}, current speed: {}' \
              .format(self.id, round(lead_distance), round(self.speed)))

        # if self.position < car2.position:    # FIXME: What if it rolls over?
        #     # TODO: Add a test for lapping
        #     if potential_position >= rear_bumper:
        #         self.stop()
        #         return True
        #     elif potential_position >= buffer_zone:
        #         self.match_speed(car2)
        #         return True

        if random.random() < self.slowing_chance:
            self.decelerate()
            return True
        else:
            return braked or False # FIXME: Avoid using braked variable, test

    def step(self, leading_car):
        self.accelerate()
        did_brake = self.brake_if_needed(leading_car)
        self.update_position(leading_car)
        return self.position, self.speed
