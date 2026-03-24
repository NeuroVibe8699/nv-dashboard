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
    # Dashboard metrics values [Ref: PDF 0.1.2]
    return jsonify({
        "status": "Online",
        "metrics": {
            "velocity": round(random.uniform(3.5, 4.8), 2),
            "acceleration": round(random.uniform(0.9, 1.3), 2),
            "temp": round(random.uniform(39.0, 42.5), 1),
            "flux": round(random.uniform(0.09, 0.11), 3),
            "rpm": random.randint(1445, 1475),
            "ultrasound": round(random.uniform(25.0, 32.0), 1)
        },
        "spectrum": [random.uniform(1, 8) for _ in range(30)]
    })

# Vercel requirement
app = app
