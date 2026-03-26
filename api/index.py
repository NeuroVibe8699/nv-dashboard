import os
import random
import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# --- DATABASE CONNECTION (Vercel Postgres) ---
def get_db_connection():
    try:
        # Vercel automatically sets POSTGRES_URL in Environment Variables
        conn = psycopg2.connect(os.environ.get('POSTGRES_URL'), cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"DB Connection Error: {e}")
        return None

# --- AI EMAIL ALERT LOGIC ---
def send_ai_alert(user_email, node_id, issue):
    # Environment Variables se email credentials uthayega
    sender = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS')
    
    if not sender or not password:
        return

    subject = f"NEUROVIBE AI ALERT - Node {node_id}"
    body = f"Critical Issue Detected: {issue}\nPlease check your dashboard: https://nvpredictive.com"
    msg = f"Subject: {subject}\n\n{body}"
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, user_email, msg)
        server.quit()
    except Exception as e:
        print(f"Email Error: {e}")

# --- MAIN API: STATUS & AI PROCESSING ---
@app.route('/api/status', methods=['GET'])
def get_status():
    node_id = request.args.get('node_id', 'NVS-1001')
    
    # 1. Pick-to-Pick Data Logic (Simulation for Real-time feel)
    metrics = {
        "velocity": round(random.uniform(3.0, 5.2), 2),
        "acceleration": round(random.uniform(0.7, 1.4), 2),
        "temp": round(random.uniform(36.0, 48.0), 1),
        "flux": round(random.uniform(0.08, 0.18), 3),
        "rpm": random.randint(1420, 1500),
        "ultrasound": round(random.uniform(22.0, 35.0), 1)
    }

    # 2. AI Autonomous Logic: Check thresholds
    alert_triggered = False
    if metrics["velocity"] > 4.6 or metrics["temp"] > 45.0:
        alert_triggered = True
        # Production: Yahan DB se user email fetch karke alert jayega
        # send_ai_alert("client@email.com", node_id, "Abnormal Vibration/Heat")

    return jsonify({
        "metrics": metrics,
        "alert": alert_triggered,
        "node": node_id,
        "status": "Online",
        "brand": "NeuroVibe AI Technologies Pvt Ltd"
    })

# --- LOGIN AUTHENTICATION ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    # Static Admin Check (Later: Sync with Postgres Users Table)
    if data.get('u') == "admin@nvpredictive.com" and data.get('p') == "admin123":
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

# --- INVENTORY & MAPPING (STUB) ---
@app.route('/api/map-device', methods=['POST'])
def map_device():
    # Admin can map Radio MAC to User ID here
    return jsonify({"message": "Device Mapped Successfully"})

if __name__ == "__main__":
    app.run()
