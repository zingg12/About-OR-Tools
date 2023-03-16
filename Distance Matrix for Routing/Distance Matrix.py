from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
from geopy.distance import distance
import numpy as np

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

distance_matrix = (distances / 1000) * 1000

print('Distance Matrix:  \n', distance_matrix)



