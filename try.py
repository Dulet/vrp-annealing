import numpy
import matplotlib.pyplot as plt
from values import values
from geopy import distance

distance = [[round(((distance.distance(tuple(x[:2]), tuple(y[:2]))).km)) for y in values] for x in values]

class Coordinate:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

def get_total_distance(coords):
    dist = 0
    for first, second in zip(coords[:-1], coords[1:]):
        dist += distance[first.index][second.index]
    dist += distance[coords[0].index][coords[-1].index]
    return dist

def plot(ax, coords):
    for first, second in zip(coords[:-1], coords[1:]):
        ax.plot([first.x, second.x], [first.y, second.y], 'b')
    ax.plot([coords[0].x, coords[-1].x], [coords[0].y, coords[-1].y], "b")
    for c in coords:
        ax.plot(c.x, c.y, 'ro')

if __name__ == "__main__":
    coords = []
    points = []
    for i, value in enumerate(values):
        points.append(i)
        coords.append(Coordinate(value[0], value[1], i))

    fig = plt.figure(figsize=(10, 5))
    ax1 = fig.add_subplot(121)
    plot(ax1, coords)

    T = 20
    FACTOR = 0.999
    T_INIT = T
    MAX_EPOCH = 50
    MAX_TRIES = 100
    VEHICLES = 5
    MAX_CAPACITY = 1000

    min_cost = get_total_distance(coords)

    for i in range(MAX_EPOCH):
        print(i, 'cost=', min_cost)
        T *= FACTOR
        for j in range(MAX_TRIES):
            temppoints = points
            capacity = MAX_CAPACITY
            attempts = 10
            r1 = 0
            while VEHICLES > 0:
                r2 = numpy.random.choice(temppoints)
                coords[r1], coords[r2] = coords[r2], coords[r1]
                new_cost = get_total_distance(coords)
                if capacity >= 0 or attempts >= 0:
                    if new_cost < min_cost or (numpy.random.uniform() < numpy.exp((min_cost - new_cost) / T)):
                        if (capacity - values[r2][2] >= 0):
                            r1 = r2
                            temppoints.remove(r2)
                            min_cost = new_cost
                            capacity -= values[r2][2]
                            print(capacity)
                        else:
                            coords[r1], coords[r2] = coords[r2], coords[r1]
                    else:
                        if attempts != 0:
                            attempts -= 1
                        else:
                            r1 = 0
                            VEHICLES -= 1
                            attempts = 10
                            capacity = MAX_CAPACITY

    ax2 = fig.add_subplot(122)
    plot(ax2, coords)
    plt.show()