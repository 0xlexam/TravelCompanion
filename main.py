from flask import Flask, request, jsonify
from flask_caching import Cache
import os
import requests

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
app.config['CACHE_TYPE'] = 'SimpleCache'
cache.init_app(app)

API_KEY = os.getenv('API_KEY')

users_bookings = {}

@app.route('/query', methods=['POST'])
@cache.cached(timeout=50, query_string=True)  # Caches for 50 seconds, could adjust depending on freshness needs
def query_destination():
    data = request.json
    destination = data.get('destination')
    if not destination:
        return jsonify({"error": "Destination not provided"}), 400
    
    # Check cache first
    cache_key = f"dest_{destination}"
    cached_dest_info = cache.get(cache_key)
    if cached_dest_info:
        return jsonify(cached_dest_info), 200

    response = requests.get(f"https://api.example.com/destinations?query={destination}&api_key={API_KEY}")
    destination_info = response.json()
    
    # Store in cache before returning
    cache.set(cache_key, destination_info, timeout=50)  # Cache this specific destination query
    
    return jsonify(destination_info), 200

@app.route('/booking', methods=['POST'])
def book_trip():
    data = request.json
    user_id = data.get('user_id')
    booking_details = data.get('booking_details')
    
    if not user_id or not booking_details:
        return jsonify({"error": "Missing booking details"}), 400
    
    response = requests.post("https://api.example.com/bookings",
                             json=booking_details,
                             headers={"Authorization": f"Bearer {API_KEY}"})
    booking_response = response.json()
    
    if response.status_code == 200:
        users_bookings[user_id] = booking_details
        return jsonify(booking_response), 200
    else:
        return jsonify(booking_response), response.status_code

@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    data = request.json
    user_id = data.get('user_id')
    booking_id = data.get('booking_id')
    
    if not user_id or not booking_id:
        return jsonify({"error": "Missing user or booking ID"}), 400
    
    response = requests.delete(f"https://api.example.com/bookings/{booking_id}",
                               headers={"Authorization": f"Bearer {API_KEY}"})
    if response.status_code == 200:
        del users_bookings[user_id]  # Consider checking if user_id exists before deleting
        return jsonify({"message": "Booking cancelled successfully"}), 200
    else:
        return jsonify({"error": "Failed to cancel booking"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)