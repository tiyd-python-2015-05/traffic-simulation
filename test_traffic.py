from traffic import *

my_car = Car(0)

Ncars = 30
positions = np.linspace(0, 1000, num=Ncars+1)
cars = [Car(positions[i]) for i in range(Ncars)]
for i in range(Ncars-1):
    cars[i].set_next(cars[i+1])
cars[Ncars-1].set_next(cars[0])



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
        car2.advance_time()
#        print(car.space())
        car.move()
#        print(str(car)+ " "+str(car2)+" "+str(car.space()))
    assert car.pos < car2.pos

def test_dist_consistency():

    tol = 1.0e-4
    sim = Simulation(cars)

    for i in range(10):
        sim.run_once()
    assert 1000-tol <= sim.dist_array().sum()+5*30 <= 1000 + tol

def test_create_hard():

    simz = Simulation(30, True)
    print(simz.N)
    assert simz.N == 7*30

def test_hard_cars():

    simz = Simulation(30, True)
    assert len(simz.dist_array()) == 7*30

def test_nightmare_cars():

    simx = Simulation(30, False, True) # normal + nightmare

    int_count = 0
    for x in simx.cars:
        if type(x) is not Car:
            int_count += 1

    assert int_count == 0


def test_nightmare_cars2():

    simx = Simulation(30, True, True) # hard + nightmare

    int_count = 0
    for x in simx.cars:
        if type(x) is not Car:
            int_count += 1

    assert int_count == 0
