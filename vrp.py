import random
import copy

def calculate_route_distance(route_nodes, distances_matrix):
    dist = 0.0
    for i in range(len(route_nodes) - 1):
        from_node = route_nodes[i]
        to_node = route_nodes[i+1]
        # Asegurarse de que los índices son válidos
        dist += distances_matrix[from_node][to_node]
    
    return dist

def two_opt_route(route_nodes, distances_matrix):
    """
    Optimiza una única ruta usando el algoritmo 2-Opt.
    La ruta debe ser una lista de índices de nodos, ej: [D, C1, C2, D].
    """
    if len(route_nodes) < 4: # No se puede aplicar 2-Opt a rutas con menos de 2 clientes
        return route_nodes

    best_route = copy.deepcopy(route_nodes)
    best_distance = calculate_route_distance(best_route, distances_matrix)
    
    improved = True
    while improved:
        improved = False
        for i in range(len(best_route) - 3): # El nodo route[i]
            for j in range(i + 2, len(best_route) - 1): # El nodo route[j]
                # Costo actual de las dos aristas que se eliminarían:
                cost_current_edges = distances_matrix[best_route[i]][best_route[i+1]] + \
                                     distances_matrix[best_route[j]][best_route[j+1]]
                
                # Costo de las dos nuevas aristas que se añadirían:
                cost_new_edges = distances_matrix[best_route[i]][best_route[j]] + \
                                 distances_matrix[best_route[i+1]][best_route[j+1]]

                if cost_new_edges < cost_current_edges:
                    # Realizar el intercambio (invertir el segmento)
                    new_route_segment_reversed = best_route[i+1:j+1][::-1]
                    current_best_route_copy = best_route[:i+1] + new_route_segment_reversed + best_route[j+1:]

                    best_route = current_best_route_copy
                    # La nueva distancia total se puede calcular incrementalmente o completamente
                    best_distance += (cost_new_edges - cost_current_edges)
                    improved = True
        
        if not improved:
            break
            
    return best_route


def clarke_wright_savings(distances_matrix, vehicle_capacity, num_customers, depot_node=0, noise_factor=0.0):
    if not distances_matrix or num_customers == 0:
        return [], 0.0

    customer_nodes = list(range(1, num_customers + 1)) 

    active_routes = []
    customer_to_route_idx = {} 

    for i, cust_idx in enumerate(customer_nodes):
        route_obj = {
            'nodes': [depot_node, cust_idx, depot_node],
            'load': 1, 
            'active': True,
            'id': i 
        }
        active_routes.append(route_obj)
        customer_to_route_idx[cust_idx] = i

    savings_list = []
    for i_idx_in_customers, cust_i in enumerate(customer_nodes):
        for j_idx_in_customers in range(i_idx_in_customers + 1, num_customers):
            cust_j = customer_nodes[j_idx_in_customers]
            
            dist_depot_i = distances_matrix[depot_node][cust_i]
            dist_depot_j = distances_matrix[depot_node][cust_j]
            dist_i_j = distances_matrix[cust_i][cust_j]
            
            saving_original = dist_depot_i + dist_depot_j - dist_i_j
            
            perturbation = saving_original * random.uniform(-noise_factor, noise_factor)
            perturbed_saving_value = saving_original + perturbation
            
            if saving_original > 0: 
                savings_list.append({
                    'value': perturbed_saving_value,
                    'original_value': saving_original,
                    'i': cust_i, 
                    'j': cust_j
                })

    savings_list.sort(key=lambda x: x['value'], reverse=True)

    for saving_entry in savings_list:
        cust_i = saving_entry['i']
        cust_j = saving_entry['j']

        route_idx_i = customer_to_route_idx.get(cust_i)
        route_idx_j = customer_to_route_idx.get(cust_j)

        if route_idx_i is None or route_idx_j is None or \
           not active_routes[route_idx_i]['active'] or \
           not active_routes[route_idx_j]['active'] or \
           route_idx_i == route_idx_j:
            continue

        route1 = active_routes[route_idx_i]
        route2 = active_routes[route_idx_j]
        merged_successfully = False

        # Caso 1: Fin de ruta1 (cust_i) se une al inicio de ruta2 (cust_j)
        if route1['nodes'][-2] == cust_i and route2['nodes'][1] == cust_j:
            if route1['load'] + route2['load'] <= vehicle_capacity:
                new_nodes = route1['nodes'][:-1] + route2['nodes'][1:]
                new_load = route1['load'] + route2['load']
                
                active_routes[route_idx_i]['nodes'] = new_nodes
                active_routes[route_idx_i]['load'] = new_load
                active_routes[route_idx_j]['active'] = False
                for node_in_old_route2 in route2['nodes'][1:-1]:
                    customer_to_route_idx[node_in_old_route2] = route_idx_i
                merged_successfully = True
        
        # Caso 2: Fin de ruta2 (cust_j) se une al inicio de ruta1 (cust_i)
        elif not merged_successfully and route2['nodes'][-2] == cust_j and route1['nodes'][1] == cust_i:
             if route1['load'] + route2['load'] <= vehicle_capacity:
                new_nodes = route2['nodes'][:-1] + route1['nodes'][1:] # ruta2 seguida de ruta1
                new_load = route1['load'] + route2['load']

                active_routes[route_idx_i]['nodes'] = new_nodes 
                active_routes[route_idx_i]['load'] = new_load
                active_routes[route_idx_j]['active'] = False
                for node_in_old_route2 in route2['nodes'][1:-1]: # Nodos de la ex-ruta2 ahora pertenecen a ruta_idx_i
                    customer_to_route_idx[node_in_old_route2] = route_idx_i
                merged_successfully = True
        
        # Caso 3: Inicio de ruta1 (cust_i) se une al inicio de ruta2 (cust_j)
        # Implica invertir una de las rutas. Ej: invertir ruta1 y unir su nuevo final (cust_i) al inicio de ruta2 (cust_j)
        elif not merged_successfully and route1['nodes'][1] == cust_i and route2['nodes'][1] == cust_j:
            if route1['load'] + route2['load'] <= vehicle_capacity:
                # Invertir clientes de ruta1: D-i-...-x-D  =>  D-x-...-i-D
                # Unir D-x-...-i  con  j-...-y-D
                reversed_route1_clients = route1['nodes'][-2:0:-1] # Clientes de ruta1 en orden inverso
                new_nodes = [depot_node] + reversed_route1_clients + route2['nodes'][1:]
                new_load = route1['load'] + route2['load']

                active_routes[route_idx_i]['nodes'] = new_nodes
                active_routes[route_idx_i]['load'] = new_load
                active_routes[route_idx_j]['active'] = False
                for node_in_old_route2 in route2['nodes'][1:-1]:
                    customer_to_route_idx[node_in_old_route2] = route_idx_i
                merged_successfully = True

        # Caso 4: Fin de ruta1 (cust_i) se une al fin de ruta2 (cust_j)
        # Implica invertir una de las rutas. Ej: invertir ruta2 y unir el fin de ruta1 (cust_i) al nuevo inicio de ruta2 (cust_j)
        elif not merged_successfully and route1['nodes'][-2] == cust_i and route2['nodes'][-2] == cust_j:
            if route1['load'] + route2['load'] <= vehicle_capacity:
                reversed_route2_clients = route2['nodes'][-2:0:-1] # Clientes de ruta2 en orden inverso
                new_nodes = route1['nodes'][:-1] + reversed_route2_clients + [depot_node]
                new_load = route1['load'] + route2['load']
                
                active_routes[route_idx_i]['nodes'] = new_nodes
                active_routes[route_idx_i]['load'] = new_load
                active_routes[route_idx_j]['active'] = False
                for node_in_old_route2 in route2['nodes'][1:-1]:
                    customer_to_route_idx[node_in_old_route2] = route_idx_i
                merged_successfully = True

    # --- Aplicar 2-Opt a cada ruta generada ---
    final_routes_nodes_optimized = []
    total_distance_optimized = 0.0
    for route_obj in active_routes:
        if route_obj['active']:
            # Optimizar la ruta actual con 2-Opt
            optimized_nodes = two_opt_route(route_obj['nodes'], distances_matrix)
            route_obj['nodes'] = optimized_nodes # Actualizar con la ruta optimizada
            
            final_routes_nodes_optimized.append(optimized_nodes)
            total_distance_optimized += calculate_route_distance(optimized_nodes, distances_matrix)
            
    return final_routes_nodes_optimized, total_distance_optimized