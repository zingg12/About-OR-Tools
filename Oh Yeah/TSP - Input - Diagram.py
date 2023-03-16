import matplotlib.pyplot as plt
import numpy as np

# masukkan koordinat kota
cities = np.array([(60, 200), (180, 200), (80, 180), (140, 180), (20, 160), (100, 160), (200, 160), (140, 140), (40, 120), (100, 120), (180, 100), (60, 80), (120, 80), (180, 60), (20, 40), (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)])

# masukkan rute hasil dari Travel Salesperson Problem
route = [0, 8, 9, 5, 6, 2, 3, 1, 4, 7, 10, 11, 15, 14, 18, 19, 17, 16, 13, 12, 0]

# buat plot
plt.plot(cities[:,0], cities[:,1], 'o')

# tambahkan label ke setiap kota
for i, city in enumerate(cities):
    plt.text(city[0], city[1], str(i))

# tambahkan garis untuk menghubungkan setiap kota pada rute
for i in range(len(route)-1):
    plt.plot([cities[route[i],0], cities[route[i+1],0]], [cities[route[i],1], cities[route[i+1],1]], 'k-')

# tambahkan garis untuk menghubungkan kota terakhir ke kota pertama
plt.plot([cities[route[-1],0], cities[route[0],0]], [cities[route[-1],1], cities[route[0],1]], 'k-')

# tampilkan plot
plt.show()
