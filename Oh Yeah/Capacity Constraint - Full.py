# Capacity (VINCENTY)

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

#Add Dimension
dimension_distance = 'Distance'
routing.AddDimension(
transit_callback_index,
0,
100,
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

