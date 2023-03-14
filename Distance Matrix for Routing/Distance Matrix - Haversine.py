from math import radians, sin, cos, sqrt, atan2
from ortools.distance_callback import DistanceCallback

# koordinat geografis masing-masing kota
coords = {
    'Jakarta': (-6.21462, 106.84513),
    'Bandung': (-6.91746, 107.61912),
    'Tangerang': (-6.17830, 106.63189),
    'Bogor': (-6.59503, 106.81617),
}

# konversi derajat ke radian
r = 6371  # radius bumi dalam kilometer
coords = {k: (radians(lat), radians(lon)) for k, (lat, lon) in coords.items()}

class HaversineDistance(DistanceCallback):
    def distance(self, from_node, to_node):
        lat1, lon1 = coords[from_node]
        lat2, lon2 = coords[to_node]
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return int(r * c)

# inisialisasi distance callback
dist_callback = HaversineDistance()

# pembuatan distance matrix
num_locations = len(coords)
distance_matrix = {}

for from_node in coords.keys():
    distance_matrix[from_node] = {}
    for to_node in coords.keys():
        if from_node == to_node:
            distance_matrix[from_node][to_node] = 0
        else:
            distance_matrix[from_node][to_node] = dist_callback.distance(from_node, to_node
