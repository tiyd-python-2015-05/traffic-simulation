"""
  Road:
    Tells the car the current conditions at its position when asked
    Tells the car if it needs to reset the x position
"""

class Road():
    def __init__(self, length=1000, slowing_factor=1):
        self.length = length
        self.slowing_factor = slowing_factor

    def validate(self, position):
        return position % self.length

        # make slowing factor position dependent
