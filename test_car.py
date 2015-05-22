from car import Car, Road
from unittest import mock
from nose.tools import raises

"""
  Car:
    Must know about car in front's current position and speed
    At each time step, update position if possible
      then make decision whether to speed up, slow down, or stop,
      based on leading car's current position/speed, self's desired following distance,
      and self's current speed, desired speed, and slowing chance, and road conditions
    Car stops if continuing will cause a collision (collisions not modeled)
    Ask the Road current road condition
    Ask the Road if current position is valid or has to turn over
"""

def test_car_creation():
    car = Car()
    assert car.desired_speed == 120
    assert car.length == 5
    assert car.accel_rate == 2
    assert -0.01 < car.slowing_chance - 0.1 < 0.1
    assert car.decel_rate == 2

    assert car.speed == 60

    assert car.desired_spacing == car.speed

    car = Car(position=5, desired_speed=130, length=6, accel_rate=3,
                slowing_chance=0.2, decel_rate=3, init_speed=61,
                desired_spacing_factor=2)
    assert car.position == 5
    assert car.desired_speed == 130
    assert car.length == 6
    assert car.accel_rate == 3
    assert -0.01 < car.slowing_chance - 0.2 < 0.1
    assert car.decel_rate == 3

    assert car.speed == 61

    assert car.desired_spacing == car.speed * 2

def test_car_accelerate():
    car = Car()
    assert car.speed == 60
    car.accelerate()
    assert car.speed == 62

def test_car_stop():
    car = Car()
    assert car.speed == 60
    car.stop()
    assert car.speed == 0

def test_update_position():
    car = Car(init_speed=100)
    assert car.position == 0 and car.speed == 100
    car.update_position()
    assert car.position == 0 + car.m_per_s * car.s_per_step

def test_brake_if_needed():
    # Stop if collision imminent
    car1 = Car(position=200, init_speed=100)
    car2 = Car(position=210)
    did_brake = car1.brake_if_needed(car2)
    assert did_brake is True
    assert car1.speed == 0

def test_match_speed():
    car1 = Car(position=200, init_speed=100)
    car2 = Car(position=230)
    assert car2.speed == 60 != car1.speed
    car1.match_speed(car2)
    assert car1.speed == car2.speed == 60

    car1 = Car(position=200, init_speed=100)
    car2 = Car(position=240)
    assert car2.speed == 60 != car1.speed
    car1.brake_if_needed(car2)
    assert car1.speed == car2.speed == 60

def test_car_slows_if_over_desired_speed():
    car1 = Car(init_speed=100, desired_speed=60)
    car2 = Car(position=900)
    with mock.patch("random.random", return_value=1):
        # disable random braking
        car1.brake_if_needed(car2)
    assert car1.speed == 60

    with mock.patch("random.random", return_value=0.05):
        # force random braking
        car1.brake_if_needed(car2)
    assert car1.speed == 58

    car1.speed = 100
    car1.accelerate()
    assert car1.speed == 60

def test_car_decelerate():
    car = Car()
    assert car.speed == 60
    car.decelerate()
    assert car.speed == 58
    car.speed = 1
    car.decelerate()
    assert car.speed == 0

def test_step():
    # Stop if collision imminent
    car1 = Car(position=200, init_speed=100)
    car2 = Car(position=210)
    car1.step(car2)
    assert car1.speed == 0

    car1 = Car(position=200, init_speed=100)
    car2 = Car(position=240)
    car1.step(car2)
    assert car1.speed == car2.speed

    car1 = Car(position=200, init_speed=100)
    car2 = Car(position=400)
    with mock.patch("random.random", return_value=1):
        car1.step(car2)
    assert car1.speed == 102

def test_accel_and_decel_are_mutually_exclusive():
    for _ in range(100):
        with mock.patch("random.random", return_value=1):
            car1 = Car(position=200, init_speed=100)
            car2 = Car(position=400)
            car1.step(car2)
            assert car1.speed == 102 or car1.speed == 98

@raises(TypeError)
def test_car_requires_road():
    car = Car()


def test_car_is_validating_position_with_road():
    assert False

# Add road with looping zero
# Add pytest and nose to requirements.txr
