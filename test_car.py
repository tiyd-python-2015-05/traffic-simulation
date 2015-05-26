from car import Car, TeleportationError
from road import Road
from unittest import mock
from nose.tools import raises


### Note that this assumed we would be going through the cars array in
### reverse order

def test_car_creation():
    road = Road()
    car = Car(road)
    assert car.desired_speed == 33.333
    assert car.length == 5
    assert car.accel_rate == 2
    assert -0.01 < car.slowing_chance - 0.1 < 0.1
    assert car.decel_rate == 2
    assert car.s_per_step == 1

    assert car.speed == 15

    assert car.desired_spacing == car.speed

    car = Car(road, position=5, desired_speed=40, length=6, accel_rate=3,
                slowing_chance=0.2, decel_rate=3, init_speed=20,
                desired_spacing_factor=2, s_per_step= 1)
    assert car.position == 5
    assert car.desired_speed == 40
    assert car.length == 6
    assert car.accel_rate == 3
    assert -0.01 < car.slowing_chance - 0.2 < 0.1
    assert car.decel_rate == 3

    assert car.speed == 20

    assert car.desired_spacing == car.speed * 2
    assert car.id == 1
    car2 = Car(road)
    assert car2.id == 2

def test_car_accelerate():
    road = Road()
    car = Car(road)
    assert car.speed == 15
    car.accelerate()
    assert car.speed == 17

def test_car_stop():
    road = Road()
    car = Car(road)
    assert car.speed == 15
    car.stop()
    assert car.speed == 0

def test_update_position():
    road = Road()
    car = Car(road, init_speed=10)
    car2 = Car(road, position=500)
    assert car.position == 0 and car.speed == 10
    car.update_position(car2)
    assert car.position == 0 + car.speed * car.s_per_step

def test_brake_if_needed():
    # Stop if collision imminent
    road = Road()
    car1 = Car(road, position=200, init_speed=20)
    car2 = Car(road, position=210)
    with mock.patch("random.random", return_value=1):
        did_brake = car1.brake_if_needed(leading_car=car2)
    assert did_brake is True
    assert car1.speed == 5


def test_car_slows_if_over_desired_speed():
    road = Road()
    car1 = Car(road, init_speed=100, desired_speed=30)
    car2 = Car(road, position=900)
    with mock.patch("random.random", return_value=1):
        # disable random braking
        car1.brake_if_needed(leading_car=car2)
    assert car1.speed == 30

    with mock.patch("random.random", return_value=0.05):
        # force random braking
        car1.brake_if_needed(leading_car=car2)
    assert car1.speed == 28

    car1.speed = 100
    car1.accelerate()
    assert car1.speed == 30

def test_car_decelerate():
    road = Road()
    car = Car(road)
    assert car.speed == 15
    car.decelerate()
    assert car.speed == 13
    car.speed = 1
    car.decelerate()
    assert car.speed == 0

def test_step_speed():
    road = Road()
    car1 = Car(road, position=1000, init_speed=15)
    car2 = Car(road, position=10)
    with mock.patch("random.random", return_value=1):
        car1.step_speed(car2)
    assert car1.speed == 5

    car1 = Car(road, position=200, init_speed=15)
    car2 = Car(road, position=223) # just enough room to speed up
    with mock.patch("random.random", return_value=1):
        car1.step_speed(car2)
    assert car1.speed == 17

    car1 = Car(road, position=200, init_speed=10)
    car2 = Car(road, position=400)
    with mock.patch("random.random", return_value=1):
        car1.step_speed(car2)
    assert car1.speed == 12

# Undecided these don't need to be mutually exclusive
def test_accel_and_decel_are_mutually_exclusive():
    road = Road()
    for _ in range(100):
        with mock.patch("random.random", return_value=1):
            car1 = Car(road, position=200, init_speed=10)
            car2 = Car(road, position=400)
            car1.step_speed(car2)
            assert car1.speed == 12 or car1.speed == 8

@raises(TypeError)
def test_car_requires_road():
    car = Car()


def test_car_is_validating_position_with_road():
    # On init
    road = Road()
    car1 = Car(road, position=2000)
    assert car1.position == 0

    # In update_position
    car1 = Car(road, position=100, init_speed=10)
    car2 = Car(road, position=500)
    car1.position = 1000
    car1.update_position(car2)
    assert car1.position == 10

    # In brake_if_needed
    car1 = Car(road, position=1005, init_speed=10)
    car2 = Car(road, position=10)
    did_brake = car1.brake_if_needed(leading_car=car2)
    assert did_brake is True

    with mock.patch("random.random", return_value=1):
        car1 = Car(road, position=500, init_speed=10)
        car2 = Car(road, position=0)
        did_brake = car1.brake_if_needed(leading_car=car2)
        assert did_brake is False

    assert car1.distance_behind(car2) == 495

@raises(TeleportationError)
def test_car_has_jumped_ahead():
    road = Road()
    car1 = Car(road, position=5)
    car2 = Car(road, position=0)
    car2.update_position(car1)

def test_car_is_already_ahead_no_teleportation_error():
    road = Road()
    car1 = Car(road, position=5, init_speed=10, slowing_chance=0)
    car2 = Car(road, position=0, init_speed=36)
    car1.update_position(car2)
    assert car1.position == 15.0

# Add test - when testing if car should accelerate, a car should never be
# going faster than the distance between it and the next car
# Add exception if car passes through another
# Add pytest and nose to requirements.txt
# What about the speed limit?
