import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c  # km

def estimate_fare(lat1, lon1, lat2, lon2):
    base_rate = 0.8  # currency per km
    start_fee = 2.0  # flat start fee
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    return round(start_fee + (distance * base_rate), 2)
