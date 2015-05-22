import pytest
import numpy as np
from car import Car
from simulation import Simulation


car1 = Car()
car2 = Car()
car3 = Car()
car4 = Car()
cars = [car1, car2, car3, car4]

def test_simulation_takes_cars():
    sim = Simulation(cars)
    assert sim.cars == [car1, car2, car3, car4]


def test_simulation_has_length():
    sim = Simulation(cars)
    assert sim.length == 1000


def test_create_speed_matrix():
    sim = Simulation(cars)
    sim.create_empty_data_matrix()
    assert (sim.data_matrix.size) == 7200
    assert (sim.data_matrix.shape) == (2, 120, 30)


def test_setup():
    sim = Simulation(cars)
    sim.create_starting_array()
    sim_setup = sim.create_starting_array()
    assert sim_setup.size == 4
    assert sim_setup.shape == (4,)

def test_cars_get_starting_spots():
    sim = Simulation(cars)
    sim.create_empty_data_matrix(num=2, rows=120, col=4)
    start_setup = sim.give_cars_starting_places()
    assert (sim.cars[0]).location == 5
    assert (sim.cars[1]).location == 335
    assert np.array_equal(start_setup, [5, 335, 665, 995])
    assert sim.data_matrix.shape == (2, 120, 4)
    assert sim.data_matrix[0].shape == (120, 4)
    assert sim.data_matrix[0][0].shape == (4,)
    assert sim.turn_count == 1



