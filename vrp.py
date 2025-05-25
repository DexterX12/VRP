from tsp import calculate_distance, two_opt
import math
import random

def get_total_distance(routes):
    total_distance = 0

    for route in routes:
        total_distance += route[1]

    return total_distance

def calculate_polar_angle(depot, customer):
    dy = customer[1] - depot[1]
    dx = customer[0] - depot[0]

    return math.atan2(dy, dx)

def calculate_vrp(coords, distances, vehicle_capacity):
    # node clustering, based on how much a vehicle can hold
    depot = coords[0]
    customers = [i for i in range(1, len(coords))]

    # randomized polar for finding possible better routes
    customers_angles = [(i, calculate_polar_angle(depot, coords[i]) + random.gauss(0, 0.02)) for i in customers]
    sorted_customers = [i for i, _ in sorted(customers_angles, key=lambda x: x[1])]
    routes = list()

    # create n groups depending on the vehicle capacity
    groups = [
        sorted_customers[i:i+vehicle_capacity]
        for i in range(0, len(sorted_customers), vehicle_capacity)
    ]

    for group in groups:
        route = [0] + group + [0]

        # apply 2-opt in an attempt to optimize the already-optimized-via-greedy route
        optimized_group = two_opt(route, distances)
        routes.append((optimized_group, calculate_distance(optimized_group, distances)))

    return routes