import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in km
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def calculate_fare(distance_km, time_min, base_fare=300, per_km=120, per_min=50, surge=1.0):
    total = base_fare + (distance_km * per_km) + (time_min * per_min)
    return round(total * surge, 2)
