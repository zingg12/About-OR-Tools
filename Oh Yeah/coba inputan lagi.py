# Import library OR-Tools
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Fungsi untuk menghitung jarak antar koordinat
def distance(x1, y1, x2, y2):
    return int(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 + 0.5)

# Input koordinat dari user
n = int(input("Masukkan jumlah titik koordinat: "))
x = []
y = []
for i in range(n):
    print("Titik ke", i + 1)
    x_i = float(input("Masukkan koordinat x: "))
    y_i = float(input("Masukkan koordinat y: "))
    x.append(x_i)
    y.append(y_i)

# Inisialisasi solver
solver = pywrapcp.Solver('TSP')

# Parameter solver
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

# Inisialisasi distance matrix
distance_matrix = {}
for from_node in range(n):
    distance_matrix[from_node] = {}
    for to_node in range(n):
        if from_node == to_node:
            distance_matrix[from_node][to_node] = 0
        else:
            distance_matrix[from_node][to_node] = distance(x[from_node], y[from_node], x[to_node], y[to_node])

print(distance_matrix)
# Fungsi untuk mengembalikan jarak antar node
def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return distance_matrix[from_node][to_node]

# Inisialisasi manager
manager = pywrapcp.RoutingIndexManager(n, 1, 0)

# Inisialisasi model
routing = pywrapcp.RoutingModel(manager)

# Set callback function untuk mengembalikan jarak antar node
transit_callback_index = routing.RegisterTransitCallback(distance_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# Set constraint untuk visit semua node hanya sekali
routing.AddDimension(transit_callback_index, 0, n, True, 'Distance')
distance_dimension = routing.GetDimensionOrDie('Distance')
distance_dimension.SetGlobalSpanCostCoefficient(100)

# Cari solusi optimal
solution = routing.SolveWithParameters(search_parameters)

# Output hasil
if solution:
    print('Jarak terpendek: {} kilometer'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    while not routing.IsEnd(index):
        print(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))
    print(manager.IndexToNode(index))
else:
    print('Tidak ditemukan solusi')
