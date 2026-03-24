from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/status', methods=['GET'])
def get_status():
    # Ye metrics aapke dashboard ke IDs (v, a, t, f, r, u) se match karte hain
    return jsonify({
        "status": "Online",
        "metrics": {
            "velocity": round(random.uniform(3.5, 4.5), 2),
            "acceleration": round(random.uniform(0.8, 1.2), 2),
            "temp": round(random.uniform(38.0, 42.0), 1),
            "flux": round(random.uniform(0.09, 0.11), 3),
            "rpm": random.randint(1440, 1480),
            "ultrasound": round(random.uniform(25.0, 30.0), 1)
        },
        "spectrum": [random.uniform(1, 10) for _ in range(30)]
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == "admin@neurovibe.com" and data.get('password') == "admin123":
        return jsonify({"status": "success", "user": {"role": "admin"}}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

app = app
