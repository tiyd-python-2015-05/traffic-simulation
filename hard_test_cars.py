__author__ = 'joshuahiggins'
from hard_car import Car
import pytest

def test_car_has_length():
    car = Car()
    assert car.length == 5


def test_car_has_location():
    car = Car()
    assert car.location == 0


def test_car_has_speed():
    car = Car()
    assert car.speed == 0


def test_car_can_not_go_faster_than_34():
    car = Car()
    car.speed = 33
    car.accelerate()
    assert car.speed == 34


def test_car_accelerates():
    car = Car()
    car.accelerate()
    assert car.speed == 2


def test_car_decelerates():
    car = Car()
    car.speed = 30
    car.decelerate()
    assert car.speed == 28


def test_car_can_not_go_negative():
    car = Car()
    car.speed = 0
    car.decelerate()
    assert car.speed == 0


def test_car_matches_speed_car_in_front():
    car1 = Car()
    car1.speed = 24
    car2 = Car()
    car2.speed = 20
    car1.slow_down(car2)
    assert car1.speed == 20


def test_car_checks_position_and_sets_next_speed():
    car1 = Car()
    car2 = Car()
    car1.speed = 30
    car2.speed = 25


def test_car_decides_to_slow_down():
    car1 = Car()
    car2 = Car()
    car1.speed = 25
    car2.speed = 27
    car1.location = 100
    car2.location = 80
    assert car2.calculate_slowdown(car1) == True


def test_car_does_not_slow_down():
    car1 = Car()
    car2 = Car()
    car1.speed = 25
    car2.speed = 27
    car1.location = 115
    car2.location = 80
    assert car2.calculate_slowdown(car1) == False


def test_car_that_has_looped_still_makes_car_behind_slow_down():
    car1 = Car()
    car2 = Car()
    car1.speed = 25
    car2.speed = 27
    car1.location = 2
    car2.location = 980
    assert car2.calculate_slowdown(car1) == True


def test_car_that_has_looped_does_not_make_car_behind_slow_down():
    car1 = Car()
    car2 = Car()
    car1.speed = 25
    car2.speed = 27
    car1.location = 15
    car2.location = 980
    assert car2.calculate_slowdown(car1) == False








