from car import Car
import numpy as np

class Simulation:
    def __init__(self, cars, length=1000):
        self.cars = cars
        self.length = length
        self.data_matrix = []
        self.turn_count = 0
        self.current_speeds = []
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
        self.turn_count += 1
        return start_setup

    def create_empty_data_matrix(self, num=2, rows=120, col=30):
        self.data_matrix = np.zeros((num, rows, col), dtype = "int64")


    def record_position_to_data_matrix(self):

        pass



    def advance_cars_and_record(self):
        self.current_speeds = [car.speed for car in self.cars]
        self.data_matrix[0][self.turn_count] += self.current_speeds
        for i in self.data_matrix[0][self.turn_count]:
            if i > 1000:
                i -= 1000
        for i in range(len(cars)):
            (self.cars[i]).location = self.data_matrix[0][self.turn_count][i]


    def decide_speed(self):
        for i in range(len(self.cars)):
            if i == len(self.cars):
                (self.cars[i]).set_speed(self.cars[0])
            else:
                (self.cars[i]).set_speed(self.cars[(i+1)])
        self.turn_count += 1

    def run(self):
        self.create_empty_data_matrix()
        self.give_cars_starting_places()
        while self.turn_count < 120:
            self.advance_cars_and_record()
            self.decide_speed()
        return self.data_matrix




            #i think we need car ids for this







