from traffic_sim import Car, Simulation
from unittest import mock
import pytest
import numpy as np

@pytest.fixture
def car():
    return Car()

# def test_car_has_initial_speed_of_zero():
#     car = Car()
#     assert car.speed == 0


def test_car_has_size(car):
    assert car.size == 5


def test_car_can_accelerate_by_2_meters_per_second(car):
    with mock.patch("random.random", return_value=1.0):
        assert car.accelerate(0, 1) == 2
        assert car.accelerate(2, 1) == 4


def test_car_will_not_accelerate_past_120kph(car):
    with mock.patch("random.random", return_value=1.0):
        assert car.accelerate(33, 1) == 33.3


def test_car_will_randomly_decelerate(car):
    with mock.patch("random.random", return_value=0.0):
        assert car.accelerate(10, 1) == 8
        assert car.accelerate(0, 1) == 0


def test_car_slows_down_when_too_close(car):
    with mock.patch("random.random", return_value=1.0):
        assert car.slow_down(29, 30, 20) == 20
        assert car.slow_down(30, 30 , 20) == 20
        assert car.slow_down(31, 30, 20) == 32


def test_simulation_has_road_length():
    sim = Simulation(1000)
    assert sim.road == 1000


def test_simulation_can_create_empty_array():
    sim = Simulation(1000)
    assert sim.matrix == np.zeros((2, 120, 30))
