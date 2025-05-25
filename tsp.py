def calculate_tsp_nearest_neighbor(start_point, distances):
    cities = list(range(0, len(distances)))
    n = len(cities)
    visited = [False] * n
    route = [start_point] + list()
    total_distance = 0
    
    # The starting point does not count as a "to visit" city, so start from index 1
    for i in range(1, n):
        shortest_next_city = None
        shortest_distance = float('inf')

        for j in range(n):
            current_distance = distances[route[-1]][j]
            if current_distance and not visited[j] and current_distance < shortest_distance:
                shortest_next_city = j
                shortest_distance = current_distance
        
        visited[route[-1]] = True # Put the last visited city in the route as visited
        route.append(shortest_next_city) # Add the current 
        total_distance += shortest_distance

    # add the distance between the last visited city and the starting point
    total_distance += distances[route[-1]][route[0]] 
    route.append(route[0]) # now add it to the list to be clear

    return route, total_distance

def calculate_distance (route, distances):
    total_distance = 0

    for city_index in range(len(route) - 1):
        total_distance += distances[route[city_index]][route[city_index + 1]]

    total_distance += distances[route[-1]][route[0]]
    return total_distance


def two_opt(route: list, distances: list[list]):
    shortest_distance = calculate_distance(route[:], distances)
    new_route = route[:]

    for _ in range(6):
        improved = False
        for i in range(1, len(new_route) - 2):
            for j in range(i + 1, len(new_route)):
                if j - i == 1: continue # adjacent, therefore not interchangable

                # swap edges between non-adjacent cities         
                current_route = new_route[:i] + new_route[i:j][::-1] + new_route[j:]

                # get the distance of this probably-shitty route smh
                current_distance = calculate_distance(current_route, distances)

                if (current_distance < shortest_distance): # omg it actually found one
                    shortest_distance = current_distance
                    new_route = current_route
                    improved = True
        if not improved:
            break

    return new_route