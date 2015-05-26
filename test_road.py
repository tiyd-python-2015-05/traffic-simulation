from road import Road

"""
  Road:
    Tells the car the current conditions at its position when asked
    Tells the car if it needs to reset the x position
"""

def test_road_creation():
    road = Road()
    assert road.length == 1000  # meters, not km!
    assert road.slowing_factor == 1

    road = Road(length=2000, slowing_factor=2)
    assert road.length == 2000  # meters, not km!
    assert road.slowing_factor == 2
#       This will become more complex in hard mode

def test_validate_position():
    road = Road(length=1000, slowing_factor=2)
    assert road.validate(0) == 0
    assert road.validate(1) == 1
    assert road.validate(1000) == 0
    assert road.validate(1001) == 1
    assert road.validate(2000) == 0
    assert road.validate(2001) == 1

    assert road.validate(-1) == 999

    assert road.validate(-1000) == 0
    assert road.validate(-1005) == 995
    assert road.validate(-2005) == 995

def test_hard_road_slowing_factor():
    road = Road(length=7000, slowing_factor=1, hard_road=True)
    assert road.slow_factor(position=0, car_slowing_chance=0.1) == 0.1
    assert road.slow_factor(position=500, car_slowing_chance=0.1) == 0.1
    assert road.slow_factor(position=1000, car_slowing_chance=0.1) == 0.1 * 1.4
    assert road.slow_factor(position=1500, car_slowing_chance=0.1) == 0.1 * 1.4
    assert road.slow_factor(position=2000, car_slowing_chance=0.1) == 0.1
    assert road.slow_factor(position=3500, car_slowing_chance=0.1) == 0.1 * 2.0
    assert road.slow_factor(position=5500, car_slowing_chance=0.1) == 0.1 * 1.2
    assert road.slow_factor(position=6500, car_slowing_chance=0.1) == 0.1
