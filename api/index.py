from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dashboard ko data dikhane ke liye (NeuroVibe 8699 Protocol)
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "Online",
        "company": "NeuroVibe AI Technologies",
        "metrics": {
            "rpm": 1450,
            "velocity": 4.2,
            "vibration_g": 0.85,
            "temp": 38.4,
            "flux": 0.12,
            "ultrasound": 22.5
        }
    })

# Hardware (i.MX6) se data lene ke liye logic
@app.route('/api/update', methods=['POST'])
def receive_data():
    data = request.json
    return jsonify({"message": "Data received", "status": "success"})

# Vercel ke liye Flask app export
def handler(request):
    return app(request)
