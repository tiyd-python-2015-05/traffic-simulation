from car import Car
import numpy as np

class Simulation:
    def __init__(self, cars, length=1000):
        self.cars = cars
        self.length = length
        self.data_matrix = []
        self.turn_count = 0
#        self.position_matrix = []


    def create_starting_array(self):
        """Line up cars equal distance along the road."""
        number_cars = len(self.cars)
        return np.linspace(5, 995, num=number_cars, dtype = "int64")


    def give_cars_starting_places(self):
        """Give starting place to cars."""
        start_setup = self.create_starting_array()
        for i in range(len(start_setup)):
            (self.cars[i]).location = start_setup[i]
        self.data_matrix[0][0] += start_setup
        return start_setup

    def create_empty_data_matrix(self, num=2, rows=120, col=30):
        self.data_matrix = np.zeros((num, rows, col), dtype = "int64")


    def record_position_to_data_matrix(self):

        pass



    def advance_cars(self):
        speed_list = [car.speed for car in self.cars]
        pass







