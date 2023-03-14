# TSP (VINCENTY)

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from geopy.distance import distance

# Define the locations and distances
locations = {
    'Mayora': (-6.249605, 106.977037), #0
    'BCA': (-6.190411, 106.822891), #1
    'Metro TV': (-6.202777, 106.780809), #2
    'Summarecon Mall Serpong': (-6.239488, 106.625396), #3
    'Lippo Mall Puri': (-6.194608, 106.734364), #4
    # 'UMN': (-6.18897, 106.738909), #5
    'RCTI': (-6.182880, 106.785032), #6
}

num_locations = len(locations)

distances = np.zeros((num_locations, num_locations))
for i, (location1, coords1) in enumerate(locations.items()):
    for j, (location2, coords2) in enumerate(locations.items()):
        distances[i][j] = distance(coords1, coords2).km

distance_matrix = distances.astype(int)

print('Distance Matrix:  \n', distance_matrix)

# Define the TSP problem
def create_data_model():
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

# Solve the TSP problem
def solve_tsp():
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

if __name__ == '__main__':
    solve_tsp()
