
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- GLOBAL STORAGE (Data yahan save hoga) ---
latest_data = {
    "metrics": {
        "velocity": 3.85, 
        "acceleration": 0.88, 
        "temp": 40.2, 
        "rpm": 1445, 
        "ultrasound": 27.5
    },
    "alert": False,
    "node": "NVS-1010"
}

@app.route('/api/status', methods=['GET', 'POST'], strict_slashes=False)
def get_status():
    global latest_data
    
    # 1. JAB MOBILE/HARDWARE DATA BHEJE (POST)
    if request.method == 'POST':
        try:
            input_json = request.json
            if "metrics" in input_json:
                # Data update karo
                latest_data["metrics"] = input_json["metrics"]
                latest_data["node"] = input_json.get("node_id", "NVS-1010")
                # AI Logic: Alert true karo agar Velocity > 4.5
                latest_data["alert"] = True if float(latest_data["metrics"]["velocity"]) > 4.5 else False
                
                print(f"Cloud Updated: {latest_data['metrics']['velocity']} mm/s")
                return jsonify({"status": "success", "message": "Cloud Synced"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    # 2. JAB DASHBOARD DATA MANGE (GET)
    return jsonify(latest_data)

@app.route('/api/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.json
    if data.get('u') == "admin@nvpredictive.com" and data.get('p') == "admin123":
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == "__main__":
    app.run()
