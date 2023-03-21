# VRP - Input User (VINCENTY)

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from geopy.distance import distance

num_vehicles = int(input("Masukkan Jumlah Kendaraan yang akan digunakan: "))
max_distances = int(input("Masukkan Batas Maksimum Jarak Tempuh Perjalanan (dalam Kilometer): "))
num_locations = int(input("Masukkan Jumlah Lokasi yang akan dikunjungi: "))

# Create data locations
locations = []

# Input dari user
for i in range(num_locations):
    # lat = float(input(f"Masukkan latitude lokasi ke-{i+1}: "))
    # lon = float(input(f"Masukkan longitude lokasi ke-{i+1}: "))
    # locations.append((lat, lon))
    koordinat = input(f"Masukkan koordinat lokasi ke-{i+1}: ")
    lat, lon = koordinat.split(", ")
    lat = float(lat)
    lon = float(lon)
    locations.append((lat, lon))

depot = int(input("Masukkan lokasi ke berapa yang ingin dijadikan depot: "))

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
    data['depot'] = depot
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

#Add Dimension
dimension_distance = 'Distance'
routing.AddDimension(
transit_callback_index,
0,
max_distances,
True,
dimension_distance
)
distance_dimension = routing.GetDimensionOrDie(dimension_distance)
distance_dimension.SetGlobalSpanCostCoefficient(100)

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.SAVINGS)
search_parameters.time_limit.seconds = 30
solution = routing.SolveWithParameters(search_parameters)

def print_solution(data, manager, routing, solution):
    print(f'Objective: {solution.ObjectiveValue()}')
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}km\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}km'.format(max_route_distance))


#Print Solution
if solution:
        print_solution(data, manager, routing, solution)
else:
        print('No solution found !')

