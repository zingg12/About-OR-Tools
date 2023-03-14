from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
from geopy.distance import distance

#Create data locations
locations = [
    (-6.249605, 106.977037), #0
    (-6.190411, 106.822891), #1
    (-6.202777, 106.780809), #2
    (-6.239488, 106.625396), #3
    # (-6.194608, 106.734364), #4
    # (-6.18897, 106.738909), #5
    (-6.182880, 106.785032), #6
 ]

def vincenty_distance(x1, x2):
    return distance(x1, x2).km

# Create distance matrix
num_locations = len(locations)
dist_matrix = {}
for from_node in range(num_locations):
    dist_matrix[from_node] = {}
    for to_node in range(num_locations):
        if from_node == to_node:
            dist_matrix[from_node][to_node] = 0
        else:
            dist_matrix[from_node][to_node] = vincenty_distance(locations[from_node], locations[to_node])

#Print
for i in range(num_locations):
    for j in range(num_locations):
        print('%2d' % dist_matrix[i][j], end=' ')
    print()



