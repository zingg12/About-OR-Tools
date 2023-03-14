# TSP (VINCENTY)

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from geopy.distance import distance

#User Input 
coordinates = []
n = int(input("Masukkan jumlah titik koordinat: "))
for i in range(n):
    nama_lokasi = input("Masukkan Nama Lokasi")
    coordinates.append(nama_lokasi)
    x, y = map(float, input(f"Masukkan koordinat titik {nama_lokasi} (format: x y): ").split())
    coordinates.append((x, y))

locations = {
    nama_lokasi : (coordinates)
}

print(locations)

# Define the locations and distances
num_lokasi = len(coordinates)

distances = np.zeros((num_lokasi, num_lokasi))
# for i, (location1, coords1) in enumerate(coordinates.items()):
#     for j, (location2, coords2) in enumerate(coordinates.items()):
#         distances[i][j] = distance(coords1, coords2).km

# distance_matrix = distances
# print(distance_matrix)

# # print('Distance Matrix:  \n', distance_matrix)

# # Define the TSP problem
# def create_data_model():
#     data = {}
#     data['distance_matrix'] = distance_matrix
#     data['num_vehicles'] = 1
#     data['depot'] = 0
#     return data

# # Solve the TSP problem
# data = create_data_model()
# manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
#                                            data['num_vehicles'], data['depot'])
# routing = pywrapcp.RoutingModel(manager)

# def distance_callback(from_index, to_index):
#     from_node = manager.IndexToNode(from_index)
#     to_node = manager.IndexToNode(to_index)
#     return data['distance_matrix'][from_node][to_node]

# transit_callback_index = routing.RegisterTransitCallback(distance_callback)
# routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# search_parameters = pywrapcp.DefaultRoutingSearchParameters()
# search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.SAVINGS)
# search_parameters.time_limit.seconds = 30
# solution = routing.SolveWithParameters(search_parameters)
    
# # Print the solution
# def print_solution(manager, routing, solution):
#     index = routing.Start(0)
#     plan_output = 'Route for vehicle 0:\n'
#     route_distance = 0
#     while not routing.IsEnd(index):
#         plan_output += ' {} ->'.format(manager.IndexToNode(index))
#         previous_index = index
#         index = solution.Value(routing.NextVar(index))
#         route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#     plan_output += ' {}\n'.format(manager.IndexToNode(index))
#     route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#     plan_output += 'Route distance: {} km\n'.format(route_distance)
#     print(plan_output)

# #Print Solution
# if solution :
#     print_solution(manager, routing, solution)

