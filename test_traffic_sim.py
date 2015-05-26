from traffic_sim import Car, Simulation
from unittest import mock
import pytest
import numpy as np


@pytest.fixture
def car():
    return Car()

@pytest.fixture
def sim():
    car_list = [Car() for _ in range(30)]
    return Simulation(car_list, 1000)


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
        assert car.set_speed(29, 30) == 29
        assert car.set_speed(30, 30 ) == 30
        assert car.set_speed(31, 30) == 31


def test_simulation_has_road_length(sim):
    assert sim.road == 1000


def test_simulation_can_create_empty_array(sim):
    m = np.zeros((2, 122, 30))
    assert np.array_equal(sim.values, m)


def test_simulation_initial_positions(sim):
    sim.initial_positions()
    assert np.array_equal(sim.values[0][0], np.linspace(5, 995, 30))


def test_simulation_can_take_list_of_car_objects(sim):
    assert sim.cars[0].size == 5
    assert sim.cars[1].size == 5



def test_simulation_can_find_distance_between_two_positions(sim):
    sim.values = np.array([[[10, 25], [0, 0]],[[0, 0], [0, 0]]])
    assert sim.find_distance(1, 0, 1) == 10
    sim.values = np.array([[[990, 5], [0, 0]],[[0, 0], [0, 0]]])
    assert sim.find_distance(1, 0, 1) == 10

def test_simulation_can_set_new_speeds_for_cars(sim):
    with mock.patch("random.random", return_value=1.0):
        sim.values = np.array([[[10, 25], [0, 0]],[[5, 5], [0, 0]]])
        distance = sim.find_distance(1, 0, 1)
        assert sim.get_speed(distance, 1, 0) == 7
        sim.values = np.array([[[990, 5], [0, 0]], [[5, 5], [0, 0]]])
        distance = sim.find_distance(1, 0, 1)
        assert sim.get_speed(distance, 1, 0) == 7
        sim.values = np.array([[[10, 25], [0, 0]],[[15, 5], [0, 0]]])
        distance = sim.find_distance(1, 0, 1)
        assert sim.get_speed(distance, 1, 0) == 10
    with mock.patch("random.random", return_value=0.0):
        sim.values = np.array([[[10, 25], [0, 0]],[[5, 5], [0, 0]]])
        distance = sim.find_distance(1, 0, 1)
        assert sim.get_speed(distance, 1, 0) == 3
        sim.values = np.array([[[990, 5], [0, 0]], [[5, 5], [0, 0]]])
        distance = sim.find_distance(1, 0, 1)
        assert sim.get_speed(distance, 1, 0) == 3
        sim.values = np.array([[[10, 25], [0, 0]],[[15, 5], [0, 0]]])
        distance = sim.find_distance(1, 0, 1)
        assert sim.get_speed(distance, 1, 0) == 10


def test_simulation_returns_slice():
    car_list = [Car() for _ in range(30)]
    sim = Simulation(car_list, 1000)
    assert sim.run_simulation().shape == (2, 61, 30)
    car_list = [Car() for _ in range(30*7)]
    sim = Simulation(car_list, 7000, n=661)
    assert sim.run_simulation().shape == (2, 600, 210)


def test_simulation_varies_accel_with_position():
        with mock.patch("random.random", return_value=0.13):
            car_list = [Car() for _ in range(30*7)]
            sim = Simulation(car_list, 7000, n=661)
            sim.values = np.array([[[1001, 25], [1, 0]],[[2, 5], [0, 0]]])
            print(sim.values[0][0][0])
            assert sim.get_speed(10, 1, 0) == 0