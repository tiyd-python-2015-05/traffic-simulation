from traffic import *

my_car = Car(0)


def test_magic_setters():
    my_car.pos = 5
    assert my_car.pos == 5
    my_car.length = 7
    assert my_car.length == 7

def test_rollup():
    car = Car(10)
    car2 = Car(400)
    car2.speed = 0
    car.set_next(car2)
    for i in range(40):
        car.move()
#        print(car)
    assert car.pos < 400

def test_rollup2():
    car = Car(10)
    car2 = Car(400)
    car2.speed = car.top_speed / 2
    car.set_next(car2)
    for i in range(20):
        car2.pos = (car2.pos + car2.speed) % 1000
        car.move()
#        print(str(car)+ " "+str(car2))
    assert car.pos < car2.pos

def test_rollup3():
    car = Car(800)
    car2 = Car(900)
    car2.speed = car.top_speed / 2
    car.set_next(car2)
    for i in range(40):
        car2.pos = (car2.pos + car2.speed) % 1000
#        print(car.space())
        car.move()
#        print(str(car)+ " "+str(car2)+" "+str(car.space()))
    assert car.pos < car2.pos
