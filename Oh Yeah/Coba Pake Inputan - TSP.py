# TSP - Input User (VINCENTY)

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from geopy.distance import distance

num_locations = int(input("Masukkan Jumlah Lokasi yang akan dikunjungi: "))

# Create data locations
locations = []

# Input dari user
for i in range(num_locations):
    lat = float(input(f"Masukkan latitude lokasi ke-{i+1}: "))
    lon = float(input(f"Masukkan longitude lokasi ke-{i+1}: "))
    locations.append((lat, lon))

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
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

# Create model
data = create_data_model()
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
routing = pywrapcp.RoutingModel(manager)

def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.SAVINGS)
search_parameters.time_limit.seconds = 30
solution = routing.SolveWithParameters(search_parameters)
    
# Print the solution
def print_solution(manager, routing, solution):
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += 'Route distance: {} km\n'.format(route_distance)
    print(plan_output)

#Print Solution
if solution :
    print_solution(manager, routing, solution)

