import numpy as np

"""
  Simulation:
    Is passed in a set of cars X and a roadX
    Advances the step count and polls each car's position, and
      reports the next car's position to each car
    Saves position of each car into a time x road position numpy array
    Returns the numpy array after the appropriate number of steps
"""

class Simulation():
    def __init__(self, cars, steps=60):
        self.cars = cars
        self.steps = steps
        self.current_step = 0
        self.step_positions = []
        self.step_speeds = []
        self.position_array = np.empty((0, len(cars)), float)
        self.speed_array = np.empty((0, len(cars)), float)

    def get_locations_speeds(self):
        self.step_positions = []
        self.speeds = []
        for car in self.cars:
            self.step_positions.append(car.position)
#        print('step_positions: :', self.step_positions)
        # print(self.position_array)
        # print(np.array([positions]))
        # self.position_array = np.append(self.position_array,
        #                               np.array([positions[::-1]]), axis=0)
        return self.step_positions
        # RETURN step_speeds

    def start(self):
        self.get_locations_speeds()
        self.position_array = np.append(self.position_array,
                              np.array([self.step_positions]),
                              axis=0)
        self.step_positions = self.step()
        self.position_array = np.append(self.position_array,
                              np.array([self.step_positions]),
                              axis=0)
        return self.step_positions
        # FIXME: Duplicated from run() -- do we need first_step returned

    def step(self):
        for index, car in enumerate(self.cars):
            next_car = self.cars[self.valid_index(index - 1)]
            car.step(next_car)
#            print(car)
        return self.get_locations_speeds()


    def valid_index(self, index):
        num_cars = len(self.cars)
        return index % num_cars if (index > num_cars - 1 or
                                    index < 0) else index
    def run(self):
        for n in range(self.steps - 1):  # - self.current_step):
#            print('n: {} steps: {}'.format(n, self.steps))
            self.current_step = n
            self.step_positions = self.step()
            self.position_array = np.append(self.position_array,
                                  np.array([self.step_positions]),
                                  axis=0)
#            print('run step_positions: ', repr(self.step_positions))
#            print(self.position_array)
        return self.position_array

#
