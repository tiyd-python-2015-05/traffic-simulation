from car import Car
import numpy as np

class Simulation:
    def __init__(self, num_cars=30, length=1000):
        self.num_cars = num_cars
        self.cars = []
        self.length = length
        self.data_matrix = []
        self.turn_count = 0
        self.current_speeds = []


    def create_cars(self, num=30):
        """Creates cars and puts them in self.cars list."""
        for i in range(num):
            self.cars.append(Car())


    def create_starting_array(self):
        """Line up cars equal distance along the road."""
        number_cars = len(self.cars)
        return np.linspace(5, 995, num=number_cars, dtype = "int64")


    def give_cars_starting_places(self):
        """Give starting location to cars.  Sets self.data_matrix for position at 0.
        Increases turn count to 1."""
        start_setup = self.create_starting_array()
        for i in range(len(start_setup)):
            (self.cars[i]).location = start_setup[i]
        self.data_matrix[0][0] += start_setup
        self.turn_count += 1
        return start_setup


    def create_empty_data_matrix(self, num=2, rows=121):
        """Creates empty matrix for simulation"""
        self.data_matrix = np.zeros((num, rows, self.num_cars), dtype = "int64")


    def advance_cars_and_record(self):
        """Sets new car location in data matrix based on current speed.
        Changes location in cars. Tests to see if any cars have crossed 1000."""
        self.data_matrix[0][self.turn_count] = self.data_matrix[0][self.turn_count - 1] \
                                               + self.data_matrix[1][self.turn_count - 1]
        for i in np.nditer(self.data_matrix[0][self.turn_count], op_flags=['readwrite']):
            if i > 1000:
                i -=1000
        for i in range(len(self.cars)):
            (self.cars[i]).location = self.data_matrix[0][self.turn_count][i]


    def decide_speed_and_record(self):
        """Cars set speed based on position of car in front of them."""
        for i in range(len(self.cars)):
            if i == len(self.cars) - 1:
                (self.cars[i]).set_speed(self.cars[0])
            else:
                (self.cars[i]).set_speed(self.cars[(i+1)])
 #       speed_list = [car.speed for car in self.cars]
        self.data_matrix[1][self.turn_count] = [car.speed for car in self.cars]


    def run(self):
        """Runs simulation for setup, 60 seconds of getting cars to speed,
        and 60 seconds of test data."""
        self.create_cars(self.num_cars)
        self.create_empty_data_matrix()
        self.give_cars_starting_places()
        while self.turn_count < 121:
            self.advance_cars_and_record()
            self.decide_speed_and_record()
            self.turn_count += 1
        return self.data_matrix


def n_simulations(n=1000, num_cars=30):
    """Runs simulation for n trials.  Returns matrix of speeds and locations
    at all time data points."""
    sim_list = []
    matrix_list = []
    for i in range(n):
        sim_list.append(Simulation(num_cars=num_cars))
    for sim in sim_list:
        matrix_list.append(sim.run())
    return matrix_list





