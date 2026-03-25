from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import random
import uuid

app = Flask(__name__)
CORS(app)

# 1. Login Logic
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == "admin@neurovibe.com" and data.get('password') == "admin123":
        return jsonify({"status": "success", "role": "admin"}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

# 2. Live Status & Spectrum (PDF Logic Page 2)
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "metrics": {
            "velocity": round(random.uniform(3.5, 4.5), 2),
            "acceleration": round(random.uniform(0.8, 1.2), 2),
            "temp": round(random.uniform(38.0, 42.0), 1),
            "flux": round(random.uniform(0.09, 0.11), 3),
            "rpm": random.randint(1440, 1480),
            "ultrasound": round(random.uniform(25.0, 30.0), 1)
        },
        "spectrum": [random.uniform(2, 12) for _ in range(30)] # FFT Data
    })

# 3. Inventory Import (PDF Logic Page 1)
@app.route('/api/import-inventory', methods=['POST'])
def import_inv():
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    # Logic to process SR NO, MODEL, IMEI, MAC IDs
    return jsonify({"status": "success", "message": "Inventory successfully imported from Excel!"})

# 4. Provisioning Token (PDF Logic Page 3)
@app.route('/api/generate-token', methods=['POST'])
def gen_token():
    token = "NV-" + str(uuid.uuid4().hex[:6]).upper()
    return jsonify({"token": token})

if __name__ == "__main__":
    app.run()
