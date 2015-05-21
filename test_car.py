from car import Car

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

def test_car_creation():
    car = Car()
    assert car.desired_speed == 120
    assert car.length == 5
    assert car.accel_rate == 2
    assert -0.01 < car.slowing_chance - 0.1 < 0.1
    assert car.decel_rate == 2

    assert car.speed == 60

    assert car.desired_spacing == car.speed

    car = Car(desired_speed=130, length=6, accel_rate=3,
                slowing_chance=0.2, decel_rate=3, init_speed=61,
                desired_spacing_factor=2)
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
    car.accellerate()
    assert car.speed == 62

def test_car_stop():
    car = Car()
    assert car.speed == 60
    car.stop()
    assert car.speed == 0
