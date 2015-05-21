__author__ = 'joshuahiggins'
from car import Car
import pytest

def test_car_has_length():
    car = Car()
    assert car.length == 5

def test_car_has_speed():
    car = Car()
    assert car.speed == 0

def test_car_accelerates():
    car = Car()
    car.accelerate()
    assert car.speed == 2

def test_car_decelerates():
    car = Car()
    car.speed = 30
    car.decelerate()
    assert car.speed == 28

def test_car_matches_speed_car_in_front():
    car1 = Car()
    car1.speed = 24
    car2 = Car()
    car2.speed = 20
    car1.slow_down(car2)
    assert car1.speed == 20

def test_car_checks_position_and_sets_next_speed(location_1, location_2):
    """location 1 is the location of the current car, location 2 is the location
    of the second car"""
    






