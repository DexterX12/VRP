import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import numpy as np

def plot_optimized_routes(solution, coordinates, title="Rutas Optimizadas de Vehículos"):

    vehicle_routes = solution[0]
    depot_coord = coordinates[0] 

    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(14, 10)) 

    num_vehicles = len(vehicle_routes)
    colors = cm.get_cmap('viridis', num_vehicles)(np.linspace(0, 1, num_vehicles))


    customer_x = [coord[0] for i, coord in enumerate(coordinates) if i != 0]
    customer_y = [coord[1] for i, coord in enumerate(coordinates) if i != 0]
    plt.scatter(customer_x, customer_y, c='skyblue', s=100, label='Clientes', edgecolors='black', zorder=3)
    plt.scatter(depot_coord[0], depot_coord[1], c='red', s=250, marker='*', label='Depósito', edgecolors='black', zorder=4)

    for i, (x, y) in enumerate(coordinates):
        plt.text(x + 0.1, y + 0.1, str(i), fontsize=9, ha='left', va='bottom', zorder=5)

    for i, route in enumerate(vehicle_routes):
        route_color = colors[i]
        route_coords_x = [coordinates[node_idx][0] for node_idx in route]
        route_coords_y = [coordinates[node_idx][1] for node_idx in route]

        plt.plot(route_coords_x, route_coords_y, color=route_color, linewidth=2, alpha=0.8,
                 label=f'Vehículo {i+1}' if num_vehicles > 1 else 'Ruta', zorder=2)

        for k in range(len(route) - 1):
            start_node_idx = route[k]
            end_node_idx = route[k+1]

            start_coord = coordinates[start_node_idx]
            end_coord = coordinates[end_node_idx]


            plt.arrow(
                start_coord[0], start_coord[1],
                end_coord[0] - start_coord[0], end_coord[1] - start_coord[1],
                color=route_color,
                shape='full',
                lw=0,
                length_includes_head=True,
                head_width=0.25, 
                head_length=0.35,
                alpha=0.7,
                zorder=2
            )

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel("Coordenada X", fontsize=12)
    plt.ylabel("Coordenada Y", fontsize=12)

    all_x = [c[0] for c in coordinates]
    all_y = [c[1] for c in coordinates]
    plt.xlim(min(all_x) - 1, max(all_x) + 1)
    plt.ylim(min(all_y) - 1, max(all_y) + 1)

    plt.legend(loc='best', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().set_aspect('equal', adjustable='box') 
    plt.tight_layout()
    plt.show()