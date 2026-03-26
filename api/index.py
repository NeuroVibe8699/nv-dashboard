import os, random, smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        return psycopg2.connect(os.environ.get('POSTGRES_URL'), cursor_factory=RealDictCursor)
    except: return None

@app.route('/api/status', methods=['GET'])
def get_status():
    node_id = request.args.get('node_id', 'NVS-1010')
    # Pick-to-Pick AI Simulated Data
    metrics = {
        "velocity": round(random.uniform(3.2, 5.5), 2),
        "acceleration": round(random.uniform(0.7, 1.5), 2),
        "temp": round(random.uniform(35.0, 50.0), 1),
        "flux": round(random.uniform(0.08, 0.18), 3),
        "rpm": random.randint(1420, 1510),
        "ultrasound": round(random.uniform(22.0, 38.0), 1)
    }
    # AI Alert Logic (e.g. Velocity > 4.6 mm/s)
    alert = True if metrics["velocity"] > 4.6 else False
    return jsonify({"metrics": metrics, "alert": alert, "node": node_id, "brand": "NeuroVibe AI Technologies Pvt Ltd"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if data.get('u') == "admin@nvpredictive.com" and data.get('p') == "admin123":
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Unauthorized"}), 401
