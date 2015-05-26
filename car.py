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
                desired_spacing_factor=1, s_per_step=1, verbose=False):
        self.id = next(self._ids)
        self.road = road
        self.desired_speed = desired_speed
        self.length = length
        self.accel_rate = accel_rate
        self.car_slowing_chance = slowing_chance
        self.decel_rate = decel_rate
        self.speed = init_speed
        self.desired_spacing_factor = desired_spacing_factor
        self.position = road.validate(position)
        self.s_per_step = s_per_step
        self.prev_position = self.position
        self.verbose = verbose

    @property
    def desired_spacing(self):
        return self.speed * self.desired_spacing_factor

    @property
    def slowing_chance(self):
        # TODO: Add tests for road-based slowing
        return self.road.slow_factor(position=self.position,
            car_slowing_chance=self.car_slowing_chance)

    def __repr__(self):
        return 'id:{} x:{} s:{}'.format(self.id, round(self.position,2),
                                        round(self.speed, 2))

    def d_print(self, message):
        if self.verbose:
            print(message)

    def accelerate(self):
        self.speed = self.speed + self.accel_rate
        if self.speed > self.desired_speed:
            self.speed = self.desired_speed

    def stop(self):
        self.speed = 0
        self.d_print('id#{} Stopping'.format(self.id))

    def update_position(self, leading_car):
        # leading_car = self.road.validate(car2.position)

        prev_position = self.position
        potential_position = self.potential_position()
        lead_distance = self.distance_behind(leading_car) # to check leapfrogging

        # Not needed anymore?
        # if potential_position > leading_car \
        #     and self.road.validate(self.position) < leading_car:
        #     raise TeleportationError("{} is attempting to pass through {}."
        #                              .format(self, car2))
        self.position = potential_position
        def trying_to_teleport():
            if self.position - prev_position > lead_distance and \
                self.position > leading_car.position and \
                self.road.validate(self.position + 100) > \
                self.road.validate(leading_car.position + 100):
                    return True
            return False

        if trying_to_teleport():  # Stop car if it's trying to "leapfrog"
            self.position = prev_position
            self.stop()

        if trying_to_teleport():  # If stopping didn't work, raise an exception
            raise TeleportationError("{} is attempting to pass through {}. Previous Position: {} Lead_dist: {}"
                                    .format(self, leading_car, prev_position, lead_distance))
        return self.position

    def decelerate(self):
        self.speed = self.speed - self.decel_rate * self.s_per_step
        if self.speed < 0:
            self.speed = 0
        self.d_print('id#{} Slowing'.format(self.id))

    def potential_position(self):
        return self.road.validate(self.position + self.speed *
                                  self.s_per_step)

    def distance_behind(self, leading_car):
        # TODO: Add tests
        self.position = self.road.validate(self.position)
        leading_car.position = self.road.validate(leading_car.position)
        # Note: Both cars must have same road

        # Add track length if car has looped around
        self_loop = self.road.length if self.position - \
            self.prev_position < 0 else 0
        lead_loop = self.road.length if leading_car.position - \
            leading_car.prev_position < 0 else 0

        # if self.position + self_loop > leading_car.position + lead_loop:
        #     raise TeleportationError("{} is attempting to pass through {}. sloop:{} lloop:{}"
        #                              .format(self, leading_car, self_loop, lead_loop))

        # if leading_car.position < self.position:  # Lead car has looped around
        #     return leading_car.position - leading_car.length - self.position \
        #         + self.road.length
        # else:
        #     return leading_car.position - leading_car.length - self.position
        return self.road.validate((leading_car.position + lead_loop) \
            - leading_car.length - (self.position + self_loop))
            # TODO: Verify this logic with more tests

    def brake_if_needed(self, leading_car):
        if self.speed > self.desired_speed:
            self.speed = self.desired_speed

        braked = False

        # Avoid leapfrogging
        lead_distance = self.distance_behind(leading_car)
        if self.speed > lead_distance:
            #self.speed = lead_distance # TODO: Match speed here?
            self.speed = leading_car.speed
            self.d_print("Braking")
            braked = True

        self.d_print('id#{} lead_distance {}, current speed: {}' \
              .format(self.id, round(lead_distance), round(self.speed)))

        # if self.position < car2.position:    # FIXME: What if it rolls over?
        #     # TODO: Add a test for lapping
        #     if potential_position >= rear_bumper:
        #         self.stop()
        #         return True
        #     elif potential_position >= buffer_zone:
        #         self.match_speed(car2)
        #         return True

        current_slowing_chance = self.slowing_chance * 2 \
            if braked else self.slowing_chance   # TODO: Is this desirable?

        if random.random() < current_slowing_chance:
            self.decelerate()
            return True
        else:
            return braked or False

    def step_speed(self, leading_car):
        did_brake = self.brake_if_needed(leading_car)
        if not did_brake:
            self.accelerate()
        return self.speed
