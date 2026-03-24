from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask App Initialisation
app = Flask(__name__)
CORS(app)

# 1. Login Route (HTML Login form isi se connect hoga)
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        # NeuroVibe 8699 Admin Credentials
        if username == "admin@neurovibe.com" and password == "admin123":
            return jsonify({
                "status": "success",
                "user": {"email": username, "role": "admin"}
            }), 200
        else:
            return jsonify({"error": "Invalid Credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. System Status Route (Dashboard Connectivity Check)
@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "Online",
        "company": "NeuroVibe AI Technologies",
        "version": "8699.1",
        "metrics": {
            "rpm": 1450,
            "velocity": 4.2,
            "vibration_g": 0.85,
            "temp": 38.4
        }
    })

# 3. Hardware Update Route (i.MX6 Gateway se data lene ke liye)
@app.route('/api/update', methods=['POST'])
def receive_data():
    data = request.json
    # Yahan logic hardware se data receive karega
    return jsonify({"message": "Data received successfully", "status": "success"})

# Vercel ke liye Flask app ko expose karna zaroori hai
app = app
