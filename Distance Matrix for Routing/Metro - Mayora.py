#menghitung jarak antara Metro TV dengan Mayora
#Longlat didapat dari findlatitudelongitude.com
#latitude Metro TV : -6.187152 ; longitude Metro TV : 106.75889
#latitude Mayora : -6.15856 ; longitude Mayora HQ : 106.695013

#Import Library
import math
from geopy.distance import geodesic
from geopy import Point
import pandas as pd

#create data
lat1 = -6.187152
lon1 = 106.75889
lat2 = -6.15856
lon2 = 106.695013

konversi = 111.12

#Haversine
def haversine(x1, y1, x2, y2):
    r = 6371
    d_lat = math.radians(x2 - x1)
    d_lon = math.radians(y2 - y1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(x1)) * math.cos(math.radians(x2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_haversine = r * c
    return distance_haversine
distance_haversine = haversine(lat1, lon1, lat2, lon2)

#Euclidean
d = math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
distance_euclidean = d * konversi

#Manhattan
def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)
manhattan = manhattan(lat1, lon1, lat2, lon2)
distance_manhattan = manhattan * konversi

#Vincenty
metro = Point(lat1, lon1)
mayora = Point(lat2, lon2)

distance_vincenty = geodesic(metro, mayora).km

#Vincenty
#import library
from math import radians, cos, sin, atan2, sqrt

def vincenty(p1, p2):
    # Konversi koordinat ke dalam radian
    lat1, lon1 = p1
    lat2, lon2 = p2
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Konstanta algoritma Vincenty
    a = 6378137
    f = 1/298.257223563
    b = (1-f)*a

    # Iterasi hingga konvergen
    delta_lon = lon2 - lon1
    U1 = atan2((1-f)*sin(lat1), cos(lat1))
    U2 = atan2((1-f)*sin(lat2), cos(lat2))
    L = delta_lon
    lambda_old = 0
    while True:
        sin_sigma = sqrt((cos(U2)*sin(L))**2 + (cos(U1)*sin(U2) - sin(U1)*cos(U2)*cos(L))**2)
        if sin_sigma == 0:
            return 0  # Titik awal dan akhir sama
        cos_sigma = sin(U1)*sin(U2) + cos(U1)*cos(U2)*cos(L)
        sigma = atan2(sin_sigma, cos_sigma)
        sin_alpha = cos(U1)*cos(U2)*sin(L) / sin_sigma
        cos_sq_alpha = 1 - sin_alpha**2
        if cos_sq_alpha == 0:
            cos2_sigma_m = 0
        else:
            cos2_sigma_m = cos_sigma - 2*sin(U1)*sin(U2)/cos_sq_alpha
        C = f/16*cos_sq_alpha*(4+f*(4-3*cos_sq_alpha))
        lambda_new = L + (1-C)*f*sin_alpha*(sigma + C*sin_sigma*(cos2_sigma_m + C*cos_sigma*(-1 + 2*cos2_sigma_m**2)))
        if abs(lambda_new - lambda_old) < 1e-12:
            break
        lambda_old = lambda_new

    # Hitung parameter u2 dan A dan jarak
    u2 = cos_sq_alpha*(a**2 - b**2)/(b**2)
    A = 1 + u2/16384*(4096+u2*(-768+u2*(320-175*u2)))
    B = u2/1024*(256+u2*(-128+u2*(74-47*u2)))
    delta_sigma = B*sin_sigma*(cos2_sigma_m + B/4*(cos_sigma*(-1 + 2*cos2_sigma_m**2) - B/6*cos2_sigma_m*(-3 + 4*sin_sigma**2)*(-3 + 4*cos2_sigma_m**2)))
    s = b*A*(sigma - delta_sigma)

    return s

metro = (-6.187152, 106.75889)
mayora = (-6.15856, 106.695013)
distance_vincenty = vincenty(metro, mayora) / 1000

#Visualize Data
data = {'Algoritma': ['Haversine', 'Euclidean', 'Manhattan', 'Vincenty'],
        'Jarak' : ['%.2f' % distance_haversine, '%.2f' % distance_euclidean, '%.2f' % distance_manhattan, '%.2f' % distance_vincenty]        
}
df = pd.DataFrame(data)
print('Jarak (Kilometer) Antara Metro TV dengan Mayora berdasarkan 4 Algoritma adalah: \n', df, '\n Jarak berdasarkan GMaps adalah 11km')
