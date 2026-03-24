from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    u = data.get('username')
    p = data.get('password')
    # Exact credentials as per your screenshot
    if u == "admin@neurovibe.com" and p == "admin123":
        return jsonify({"status": "success", "role": "admin"}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

@app.route('/api/status', methods=['GET'])
def get_status():
    # PDF Logic: Generating real-time metrics
    return jsonify({
        "metrics": {
            "velocity": round(random.uniform(3.5, 4.5), 2),
            "acceleration": round(random.uniform(0.8, 1.2), 2),
            "temp": round(random.uniform(38.0, 42.0), 1),
            "flux": round(random.uniform(0.09, 0.11), 3),
            "rpm": random.randint(1440, 1480),
            "ultrasound": round(random.uniform(25.0, 30.0), 1)
        }
    })

if __name__ == "__main__":
    app.run()
