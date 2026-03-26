import os, random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global Variable to store the last received data
latest_data = {
    "velocity": 0.0, "acceleration": 0.0, "temp": 0.0, "rpm": 0, "ultrasound": 0.0
}

@app.route('/api/status', methods=['GET', 'POST'], strict_slashes=False)
def get_status():
    global latest_data
    
    # Jab Mobile App se DATA AAYE (POST)
    if request.method == 'POST':
        try:
            data = request.json
            if "metrics" in data:
                latest_data = data["metrics"] # Data yahan save ho gaya!
                return jsonify({"status": "success"}), 200
        except:
            return jsonify({"status": "error"}), 400

    # Jab Dashboard DATA MANGE (GET)
    return jsonify({
        "metrics": latest_data,
        "alert": latest_data["velocity"] > 4.5,
        "node": "NVS-1010",
        "status": "Online"
    })

if __name__ == "__main__":
    app.run()

