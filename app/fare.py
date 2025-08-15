# app/fare.py
from flask import Blueprint, request, jsonify
import math

fare_bp = Blueprint('fare', __name__)

FARE_BASE = 300
FARE_PER_KM = 120
FARE_PER_MIN = 50
SURGE_MULTIPLIER = 1.0

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def calculate_fare(distance_km, time_min):
    total = FARE_BASE + (distance_km * FARE_PER_KM) + (time_min * FARE_PER_MIN)
    return round(total * SURGE_MULTIPLIER, 2)

@fare_bp.route('/calculate_fare', methods=['POST'])
def fare_endpoint():
    data = request.get_json()
    if not all(k in data for k in ['pickup_lat', 'pickup_lng', 'drop_lat', 'drop_lng']):
        return jsonify({'error': 'Missing coordinates'}), 400

    distance = haversine(
        data['pickup_lat'], data['pickup_lng'],
        data['drop_lat'], data['drop_lng']
    )
    time_min = data.get('time_min', 15)
    fare = calculate_fare(distance, time_min)
    return jsonify({'fare': fare})
