# Capacity Constraints (VINCENTY)

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from geopy.distance import distance

# Define Locations
locations = {
    'Mayora': (-6.249605, 106.977037), #0
    'BCA': (-6.190411, 106.822891), #1
    'Metro TV': (-6.202777, 106.780809), #2
    'Summarecon Mall Serpong': (-6.239488, 106.625396), #3
    'Lippo Mall Puri': (-6.194608, 106.734364), #4
    'SMB': (-6.226194, 107.001009), #5
    'RCTI': (-6.182880, 106.785032), #6
    'AEON': (-6.304409, 106.644157) # 7
}

num_locations = len(locations)

distances = np.zeros((num_locations, num_locations))
for i, (location1, coords1) in enumerate(locations.items()):
    for j, (location2, coords2) in enumerate(locations.items()):
        distances[i][j] = distance(coords1, coords2).km

distance_matrix = distances.astype(int)
print(distance_matrix)

# Create Data
def create_data_model():
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 3
    data['demands'] = [0, 3, 5, 1, 3, 6, 2, 1]
    data['vehicles_capacities'] = [7, 7, 7]
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

#Add Dimension
routing.AddDimensionWithVehicleCapacity(
    demand_callback_index,
    0,  # null capacity slack
    data['vehicles_capacities'],  # vehicle maximum capacities
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
