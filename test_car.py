from car import Car
import py.test


def test_car_size():
    my_car = Car()
    assert my_car.size ==5
    long_car = Car()
    long_car.size = 10
    assert long_car.size == 10

def test_car_accelerate():
    my_car = Car()
    my_car.accelerate()
    assert my_car.speed == 2

def test_car_above_34():
    my_car = Car()
    my_car.speed = 34
    my_car.accelerate()
    assert my_car.speed == 34

def test_car_random_decelerate():
    my_car = Car()
    my_car.speed = 30
    my_car.decelerate()
    assert my_car.speed == 28

def test_car_neagtive_speed():
    my_car = Car()
    my_car.speed = 0
    my_car.decelerate()
    assert my_car.speed == 0

def test_car_matches_front_car():
    my_car = Car()
    my_car.speed = 30
    front_car = Car()
    front_car.speed = 24
    my_car.slow_down(front_car)
    assert my_car.speed == 24

def test_calculate_slow_down():
    my_car = Car()
    car_in_front = Car()
    my_car.speed = 30
    my_car.location = 80
    car_in_front.speed = 25
    car_in_front.location = 100
    assert my_car.calculate_slow_down(car_in_front) == True
    
def test_calculate_slow_down_when_circling_the_road():
    my_car = Car()
    car_in_front = Car()
    my_car.speed = 30
    my_car.location = 980
    car_in_front.speed = 25
    car_in_front.location = 2
    assert my_car.calculate_slow_down(car_in_front) == True

def test_calculate_not_slow_down_when_circling_the_road():
    my_car = Car()
    car_in_front = Car()
    my_car.speed = 30
    my_car.location = 980
    car_in_front.speed = 25
    car_in_front.location = 20
    assert my_car.calculate_slow_down(car_in_front) == False
