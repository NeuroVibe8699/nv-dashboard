from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# NeuroVibe 8699 Logic - PDF Ref: 0.1.2
@app.route('/api/status', methods=['GET'])
def get_status():
    # Saare 6 Parameters ka Real-time Simulation
    metrics = {
        "acceleration": round(random.uniform(0.8, 1.5), 2),
        "velocity": round(random.uniform(2.5, 6.0), 2),
        "flux": round(random.uniform(0.01, 0.15), 3),
        "ultrasound": round(random.uniform(25.0, 40.0), 1),
        "temp": round(random.uniform(36.0, 55.0), 1),
        "rpm": random.randint(1440, 1485)
    }
    
    # Spectrum (FFT) Data - PDF Ref: 0.1.2 (Graph Logic)
    spectrum = [random.uniform(0.5, 8.0) for _ in range(40)]
    
    return jsonify({
        "status": "Online",
        "company": "NeuroVibe AI Technologies",
        "metrics": metrics,
        "spectrum": spectrum,
        "sites": ["Ammonia Pump", "Production Area", "Main Compressor"]
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == "admin@neurovibe.com" and data.get('password') == "admin123":
        return jsonify({"status": "success", "role": "admin", "token": "nv_8699_secure"}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

app = app
