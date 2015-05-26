"""
  Road:
    Tells the car the current conditions at its position when asked
    Tells the car if it needs to reset the x position
"""

class Road():
    def __init__(self, length=1000, slowing_factor=1, hard_road=False):
        """Takes length in meters, slowing_factor for entire road"""
        self.length = length
        self.slowing_factor = slowing_factor
        self.hard_road = hard_road

    def validate(self, position):
        return position % self.length

    def slow_factor(self, position, car_slowing_chance):
        if self.hard_road:
            if 1000 <= position < 2000: return car_slowing_chance * 1.4;
            if 3000 <= position < 4000: return car_slowing_chance * 2.0;
            if 5000 <= position < 6000: return car_slowing_chance * 1.2;
        return car_slowing_chance
