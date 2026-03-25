from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == "admin@neurovibe.com" and data.get('password') == "admin123":
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

@app.route('/api/get-token', methods=['GET'])
def get_token():
    # Har baar naya token (Dynamic)
    new_token = f"NV-{random.randint(100000, 999999)}"
    return jsonify({"token": new_token})

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"metrics": {"velocity": 4.2, "acceleration": 0.9, "temp": 40.5, "flux": 0.10, "rpm": 1450, "ultrasound": 26.5}})
