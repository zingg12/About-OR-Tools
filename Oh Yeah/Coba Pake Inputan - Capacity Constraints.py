# Capacity Constraints - Input User (VINCENTY)

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from geopy.distance import distance



num_vehicles = int(input("Masukkan Jumlah Kendaraan yang akan digunakan: "))
vehicles_capacities = []
for c in range(num_vehicles):
     capacity = int(input(f"Masukkan kapasitas pada kendaraan {c+1}:"))
     vehicles_capacities.append(capacity)

# max_distances = int(input("Masukkan Batas Maksimum Jarak Tempuh Perjalanan (dalam Kilometer): "))
num_locations = int(input("Masukkan Jumlah Lokasi yang akan dikunjungi: "))

# Create data locations
locations = []

# Input dari user
for i in range(num_locations):
    lat = float(input(f"Masukkan latitude lokasi ke-{i+1}: "))
    lon = float(input(f"Masukkan longitude lokasi ke-{i+1}: "))
    locations.append((lat, lon))

demands = []
for d in range(num_locations):
    demand_lokasi = int(input(f"Masukkan demand pada lokasi ke-{d+1}"))
    demands.append(demand_lokasi)

num_locations = len(locations)

distances = np.zeros((num_locations, num_locations))
for i, x1 in enumerate(locations):
    for j, x2 in enumerate(locations):
        distances[i][j] = distance(x1, x2).km


distance_matrix = distances
print(distance_matrix)

# Define data
def create_data_model():
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = num_vehicles
    data['demands'] = demands
    data['vehicles_capacities'] = vehicles_capacities
    data['depot'] = 0
    return data

# Create model
data = create_data_model()
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
routing = pywrapcp.RoutingModel(manager)

#Add distance callback
def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#Add capacity constraints
def demand_callback(from_index):
     from_node = manager.IndexToNode(from_index)
     return data['demands'][from_node]

demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

vehicles_capacities = list(data['vehicles_capacities'])

#Add Dimension
routing.AddDimensionWithVehicleCapacity(
    demand_callback_index,
    0,  # null capacity slack
    vehicles_capacities,  # vehicle maximum capacities
    True,  # start cumul to zero
    'Capacity')

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
search_parameters.local_search_metaheuristic = (
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
search_parameters.time_limit.FromSeconds(1)

solution = routing.SolveWithParameters(search_parameters)

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}km\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}km'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))

if solution:
    print_solution(data, manager, routing, solution)
