from time import time
from vrp import clarke_wright_savings, calculate_route_distance
from graph import plot_optimized_routes

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
    VEHICLE_CAPACITY_CW = 12
    DISTANCES_CW, COORDINATES = load_dataset()
    NUM_CUSTOMERS_CW = len(DISTANCES_CW) - 1
    DEPOT_NODE = 0
    SAVINGS_NOISE_FACTOR = 0.05 
    OPTIMIZATION_DURATION_SECONDS_CW = 10

    loop_start_time_cw = time()
    best_overall_routes_cw = None
    best_overall_cost_cw = float('inf')
    total_iterations_cw = 0
    
    while time() - loop_start_time_cw < OPTIMIZATION_DURATION_SECONDS_CW:
        current_routes, current_total_distance = clarke_wright_savings(
            DISTANCES_CW, 
            VEHICLE_CAPACITY_CW, 
            NUM_CUSTOMERS_CW, 
            DEPOT_NODE,
            noise_factor=SAVINGS_NOISE_FACTOR
        )
        
        if current_total_distance < best_overall_cost_cw:
            best_overall_cost_cw = current_total_distance
            best_overall_routes_cw = current_routes

        total_iterations_cw += 1

    print("\n--- Mejor Solución Encontrada (Clarke-Wright + 2-Opt) ---")
    print(f"Costo (Distancia Total): {best_overall_cost_cw:.2f}")
    print("Rutas:")
    num_vehicles_used_cw_final = 0
    for i, route_nodes in enumerate(best_overall_routes_cw):
        if len(route_nodes) > 2: # Ruta válida con al menos un cliente
            num_vehicles_used_cw_final += 1
            route_dist_ind = calculate_route_distance(route_nodes, DISTANCES_CW)
            clients_in_route = [node for node in route_nodes if node != DEPOT_NODE]
            print(f"  Vehículo {num_vehicles_used_cw_final}: Depósito -> {clients_in_route} -> Depósito (Distancia: {route_dist_ind:.2f}, Clientes: {len(clients_in_route)})")
    print(f"Número total de vehículos utilizados: {num_vehicles_used_cw_final}")
    print(best_overall_routes_cw)
    plot_optimized_routes(best_overall_routes_cw, COORDINATES)
