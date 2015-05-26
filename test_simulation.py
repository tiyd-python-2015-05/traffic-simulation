from car import Car
from road import Road
from simulation import Simulation
import numpy as np
from unittest import mock

#np.array_equal

"""
  Simulation:
    Is passed in a set of cars X and a roadX
    Advances the step count and polls each car's position, and
      reports the next car's position to each car
    Saves position of each car into a time x road position numpy array
    Returns the numpy array after the appropriate number of steps
"""
def setup():
    road = Road()
    car1 = Car(road, position=100, init_speed = 10, accel_rate=0)
    car2 = Car(road, position=200, init_speed = 10, accel_rate=0)
    cars = [car2, car1]  # reverse order for easier checking
    sim = Simulation(cars=cars)
    return sim

def test_simulation_creation():
    sim = setup()
    assert sim.cars[0].id - 1 == sim.cars[1].id
    assert sim.position_array.shape == sim.speed_array.shape == (0, 2)

def test_valid_index():
    sim = setup()
    assert sim.valid_index(2) == 0
    assert sim.valid_index(-1) == 1

def test_simulation_start():
    sim = setup()
    sim.start()
    print(sim.position_array)
    # assert type(sim.position_array) is np.ndarray
    # assert np.array_equal(sim.position_array, np.array([[100., 200.]]))

def test_simulation_start_and_step():
    sim = setup()
    # TODO: Add proper testing for step_speeds
    # start: np.array([[100., 200.]]))
    with mock.patch("random.random", return_value=1):
        step_positions, step_speeds = sim.start()
        assert sim.step_positions == [210, 110]
        # assert np.array_equal(sim.position_array, np.array([[100., 210.]]))
        step_positions, step_speeds = sim.step()
        assert sim.step_positions == [220, 120]
        # assert np.array_equal(sim.position_array, np.array([[110., 220.]]))

def test_simulation_run():
    sim = setup()
    sim.steps = 3
    # start: np.array([[100., 200.]]))
    with mock.patch("random.random", return_value=1):
        first_step = sim.start()
        # first_step = sim.step()
#        assert sim.step_positions == [210, 110]
        print('first_step', first_step)
#        print('np_position_array:', np.array([first_step]))
        assert np.array_equal(np.array([first_step[0]]), np.array([[210., 110.]]))
        sim.run()
        assert sim.step_positions == [230, 130]
        assert np.array_equal(sim.position_array,
                              np.array([[200., 100.],
                                        [210., 110.],
                                        [220., 120.],
                                        [230., 130.]
                                        ]))
