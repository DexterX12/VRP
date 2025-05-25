from vrp import calculate_vrp, get_total_distance
from time import time
from functools import reduce

def load_dataset():
    distances = list()
    coordinates = list()

    with open('./dataset/Coord.txt') as coords:
        for coord in coords:
            coordinates.append(tuple(coord.strip().split("\t")))
        
        coordinates = list(map(lambda coord: (float(coord[0]), float(coord[1])), coordinates))

    with open('./dataset/Dist.txt') as dists:
        for distance_line in dists:
            distances.append(distance_line.strip().split("\t"))

        for index in range(len(distances)):
            distances[index] = list(map(lambda distance: float(distance), distances[index]))
    
    return distances, coordinates

if __name__ == '__main__':
    distances, coordinates = load_dataset()
    capacity = 12
    current_time = time()
    found_routes = list()

    while time() - current_time < 115:
        vehicle_routes = calculate_vrp(coordinates, distances, capacity)
        total_distance = reduce(lambda x, y: x + y[1], vehicle_routes, vehicle_routes[0][1])

        found_routes.append((vehicle_routes, total_distance))
    
    shortest_route = min(found_routes, key=lambda x: x[1])
    print(shortest_route)