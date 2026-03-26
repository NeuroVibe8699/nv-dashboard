import os
import random
import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
# CORS enabled for all origins to prevent dashboard blocking
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- DATABASE CONNECTION ---
def get_db_connection():
    try:
        # Vercel sets this automatically in Environment Variables
        conn = psycopg2.connect(os.environ.get('POSTGRES_URL'), cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"DB Connection Error: {e}")
        return None

# --- AI EMAIL ALERT LOGIC ---
def send_ai_alert(user_email, node_id, issue):
    sender = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS')
    if not sender or not password: return

    subject = f"NEUROVIBE AI ALERT - Node {node_id}"
    body = f"Critical Issue: {issue}\nCheck Dashboard: https://nvpredictive.com"
    msg = f"Subject: {subject}\n\n{body}"
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, user_email, [msg])
        server.quit()
    except: pass

# --- MAIN API: STATUS & AI PROCESSING (FIXED 307 ERROR) ---
@app.route('/api/status', methods=['GET', 'POST'], strict_slashes=False)
def get_status():
    # 1. HANDLE DATA FROM HARDWARE/MOBILE (POST)
    if request.method == 'POST':
        try:
            data = request.json
            # Yahan data database mein save karne ka logic aayega
            print(f"Received Data: {data}")
            return jsonify({"status": "success", "message": "Data Pushed to Cloud"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    # 2. HANDLE DASHBOARD FETCH (GET)
    # Pick-to-Pick Simulation Logic
    vibration = round(random.uniform(3.2, 5.5), 2)
    metrics = {
        "velocity": vibration,
        "acceleration": round(random.uniform(0.7, 1.4), 2),
        "temp": round(random.uniform(38.0, 46.0), 1),
        "flux": round(random.uniform(0.08, 0.18), 3),
        "rpm": random.randint(1430, 1510),
        "ultrasound": round(random.uniform(22.0, 35.0), 1)
    }

    # AI Alert Trigger
    alert_triggered = True if vibration > 4.6 else False
    
    return jsonify({
        "metrics": metrics,
        "alert": alert_triggered,
        "node": request.args.get('node_id', 'NVS-1010'),
        "status": "Online",
        "brand": "NeuroVibe AI Technologies Pvt Ltd"
    })

# --- LOGIN AUTHENTICATION ---
@app.route('/api/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.json
    # Admin Credentials Sync
    if data.get('u') == "admin@nvpredictive.com" and data.get('p') == "admin123":
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Invalid Credentials"}), 401

if __name__ == "__main__":
    app.run()
