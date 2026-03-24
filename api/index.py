from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- 1. Login Logic (Iske bina "Offline" dikhayega) ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # NeuroVibe 8699 Credentials
    if username == "admin@neurovibe.com" and password == "admin123":
        return jsonify({
            "status": "success", 
            "user": {"email": username, "role": "admin"}
        }), 200
    else:
        return jsonify({"error": "Invalid Credentials"}), 401

# --- 2. System Status ---
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "Online",
        "company": "NeuroVibe AI Technologies",
        "metrics": {
            "rpm": 1450,
            "velocity": 4.2,
            "vibration_g": 0.85,
            "temp": 38.4
        }
    })

# --- 3. Hardware Data Receive ---
@app.route('/api/update', methods=['POST'])
def receive_data():
    data = request.json
    return jsonify({"message": "Data received", "status": "success"})

# Vercel Handler
def handler(request):
    return app(request)
