import math

#menghitung jarak antara kampus UMN dengan Kantor Mayora HQ
#Longlat didapat dari findlatitudelongitude.com
#latitude UMN : -6° 15' 21.9528" ; longitude UMN : 106° 37' 8.2092"
#latitude Mayora HQ : -6.15856 ; longitude Mayora HQ : 106.695013


#Haversine
#create data
lat1 = -6.257504
lon1 = 106.618165
lat2 = -6.15856
lon2 = 106.695013

def haversine(lat1, lon1, lat2, lon2):
    r = 6371 #radius bumi dalam kilometer
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_harvesine = r * c
    return distance_harvesine

distance_harvesine = haversine(lat1, lon1, lat2, lon2)
print('Jarak antara UMN dengan Mayora by Harvesine: ', distance_harvesine, 'Kilometers')

#Euclidean
d = math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
konversi = 111.12 #
distance_euclidean = d * konversi

print('Jarak antara UMN dengan Mayora by Euclidean: ', distance_euclidean, 'Kilometers')

#Manhattan 
#import library 
lat1 = -6.257504
lon1 = 106.618165
lat2 = -6.15856
lon2 = 106.695013

def distance_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)
distance_manhattan = distance_manhattan(lat1, lon1, lat2, lon2)
distance_manhattan = distance_manhattan * konversi


print('Jarak antara UMN dengan Mayora by Manhattan: ', distance_manhattan, 'Kilometers')