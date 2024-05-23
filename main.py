from flask import Flask, request, jsonify
from flask_caching import Cache
import os
import requests

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
app.config['CACHE_TYPE'] = 'SimpleCache'
cache.init_app(app)

API_KEY = os.getenv('API_KEY')

user_bookings_dict = {}

@app.route('/destination-query', methods=['POST'])
@cache.cached(timeout=50, query_string=True)
def destination_query():
    request_data = request.json
    target_destination = request_data.get('destination')
    if not target_destination:
        return jsonify({"error": "Destination not provided"}), 400
    
    cache_key = f"destination_{target_destination}"
    cached_destination_data = cache.get(cache_key)
    if cached_destination_data:
        return jsonify(cached_destination_data), 200

    destination_response = requests.get(f"https://api.example.com/destinations?query={target_destination}&api_key={API_KEY}")
    destination_data = destination_response.json()
    
    cache.set(cache_key, destination_data, timeout=50)
    
    return jsonify(destination_data), 200

@app.route('/create-booking', methods=['POST'])
def create_booking():
    request_data = request.json
    user_id = request_data.get('user_id')
    booking_info = request_data.get('booking_details')
    
    if not user_id or booking_info is None:
        return jsonify({"error": "Missing booking details"}), 400
    
    booking_api_response = requests.post("https://api.example.com/bookings",
                             json=booking_info,
                             headers={"Authorization": f"Bearer {API_KEY}"})
    booking_result = booking_api_response.json()
    
    if booking_api_response.status_code == 200:
        user_bookings_dict[user_id] = booking_info
        return jsonify(booking_result), 200
    else:
        return jsonify(booking_result), booking_api_response.status_code

@app.route('/cancel-booking', methods=['POST'])
def cancel_booking():
    request_data = request.json
    user_id = request_data.get('user_id')
    booking_identifier = request_data.get('booking_id')
    
    if not user_id or not booking_identifier:
        return jsonify({"error": "Missing user or booking ID"}), 400
    
    cancellation_response = requests.delete(f"https://api.example.com/bookings/{booking_identifier}",
                               headers={"Authorization": f"Bearer {API_KEY}"})
    if cancellation_response.status_code == 200:
        if user_id in user_bookings_dict:
            del user_bookings_dict[user_id]
        return jsonify({"message": "Booking cancelled successfully"}), 200
    else:
        return jsonify({"error": "Failed to cancel booking"}), cancellation_response.status_code

if __name__ == '__main__':
    app.run(debug=True)