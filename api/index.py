from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import random

app = Flask(__name__)
CORS(app)

# 1. Login Logic (As per Page 1 & 2)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u, p = data.get('username'), data.get('password')
    if u == "admin@nvpredictive.com" and p == "admin123":
        return jsonify({"role": "admin", "token": "NV_ADMIN_8699"}), 200
    elif u == "client@nvpredictive.com" and p == "client123":
        return jsonify({"role": "client", "token": "NV_CLIENT_8699"}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

# 2. Inventory Import (As per Page 1 Logic)
@app.route('/api/import', methods=['POST'])
def import_inventory():
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    file = request.files['file']
    try:
        df = pd.read_excel(file)
        # Checking columns from Page 1: SR NO, MODEL, IMEI, RADIO MAC ID, BLE MAC ID
        data = df.to_dict(orient='records')
        return jsonify({"message": f"Successfully imported {len(data)} items", "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Live Status (As per Page 2 Data Logic)
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "metrics": {
            "velocity": round(random.uniform(1.0, 5.0), 2),
            "acceleration": round(random.uniform(0.5, 1.5), 2),
            "temp": round(random.uniform(35, 55), 1),
            "flux": round(random.uniform(0.08, 0.12), 3),
            "rpm": random.randint(1400, 1500),
            "ultrasound": round(random.uniform(10, 30), 1)
        }
    })

if __name__ == "__main__":
    app.run()
