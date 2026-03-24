from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == "admin@neurovibe.com" and data.get('password') == "admin123":
        return jsonify({"status": "success", "user": {"role": "admin"}}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "Online",
        "metrics": {
            "velocity": round(random.uniform(2.5, 5.0), 2),
            "acceleration": round(random.uniform(0.8, 1.4), 2),
            "temp": round(random.uniform(38, 45), 1),
            "flux": round(random.uniform(0.08, 0.12), 3),
            "rpm": random.randint(1440, 1490),
            "ultrasound": round(random.uniform(22, 35), 1)
        }
    })

# Vercel ko batane ke liye ki 'app' hi main server hai
app = app
