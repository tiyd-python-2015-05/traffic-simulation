from car import Car
import numpy as np


class Simulation:

    def __init__(self, num_cars=30, length=1000):
        self.num_cars = num_cars
        self.cars = []
        self.length = length
        self.data_matrix = []
        self.turn_count = 0

    def create_cars(self, num=30):
         for i in range(num):
             self.cars.append(Car())

    def create_starting_array(self):
        """Line up cars equal distance along the road"""
        number_cars = len(self.cars)
        return np.linspace(5, 995, num=number_cars, dtype = "int64")

    def create_empty_data_matrix(self, num=2, rows=120):
        """Creates empty matric for simulation"""
        self.data_matrix = np.zeros((num, rows, self.num_cars), dtype="int64")

    def give_cars_starting_places(self):
        """Give starting place to cars and sets self.data_matrix for position at 0.
        Incrases turn by 1."""
        start_setup = self.create_starting_array()
        for i in range(len(start_setup)):
            self.cars[i].location = start_setup[i]
        self.data_matrix[0][0] += start_setup #not working - can't get test to pass
        self.turn_count +=1
        return start_setup

    def advance_cars_and_record(self):
        """Advances cars in matrix by adding current location and speed. Changes locaiton in cars. Tests if cars have
         passed 1000m."""
        self.data_matrix[0][self.turn_count] = self.data_matrix[0][self.turn_count - 1] +\
                                               self.data_matrix[1][self.turn_count - 1]
        for i in np.nditer(self.data_matrix[0][self.turn_count], op_flags=['readwrite']):
            if i > 1000:
                i -= 1000
        for i in range(len(self.cars)):
            self.cars[i].location = self.data_matrix[0][self.turn_count][i]

    def decide_speed_and_record(self):
        """ """
        for i in range(len(self.cars)):
            if i == len(self.cars) - 1:
                self.cars[i].set_speed(self.cars[0])
            else:
                self.cars[i].set_speed(self.cars[i+1])
        speed_list = [car.speed for car in self.cars]
        self.data_matrix[1][self.turn_count] = speed_list
#in the main function that runs the program make sure to include self.turn_count +=1 after decide_speed_and_record

    def run(self):
        pass
