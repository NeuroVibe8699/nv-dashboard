from flask import Flask, request, jsonify
from flask_cors import CORS
import random, smtplib

app = Flask(__name__)
CORS(app)

# --- AI Alert & Email Function ---
def send_ai_email(user_email, node_id, issue):
    msg = f"Subject: NEUROVIBE AI CRITICAL ALERT\n\nNode {node_id} detected {issue}. Check Dashboard!"
    # Add your SMTP details here later
    print(f"Alert sent to {user_email}")

@app.route('/api/status', methods=['GET'])
def get_status():
    node_id = request.args.get('node_id', 'NVS-1001')
    # Pick-to-Pick Data Logic
    metrics = {
        "velocity": round(random.uniform(3.0, 4.5), 2),
        "acceleration": round(random.uniform(0.7, 1.1), 2),
        "temp": round(random.uniform(37.0, 42.0), 1),
        "flux": round(random.uniform(0.08, 0.12), 3),
        "rpm": random.randint(1440, 1480),
        "ultrasound": round(random.uniform(24.0, 29.0), 1)
    }
    # AI Logic Check
    alert = True if metrics["velocity"] > 4.3 else False
    return jsonify({"metrics": metrics, "alert": alert, "node": node_id})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('u') == "admin@nvpredictive.com" and data.get('p') == "admin123":
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid"}), 401

