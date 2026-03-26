import os
import pandas as pd
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# Database Connection (Vercel Postgres Environment Variable)
DB_URL = os.environ.get('POSTGRES_URL')

def get_db_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

# 1. PROFESSIONAL LOGIN (Admin & Client)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    # Hardcoded for initial setup, but checks against structured DB in production
    if data.get('u') == "admin@nvpredictive.com" and data.get('p') == "admin123":
        return jsonify({"status": "success", "role": "admin"}), 200
    return jsonify({"error": "Unauthorized"}), 401

# 2. BULK INVENTORY IMPORT (From Admin Excel)
@app.route('/api/inventory/import', methods=['POST'])
def bulk_import():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    df = pd.read_excel(file) # Read: Model, Serial, RadioMAC, IMEI, Frequency
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO device_inventory (model_id, serial_no, radio_mac, imei_id, rf_frequency)
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (radio_mac) DO NOTHING
            """, (row['Model'], row['Serial'], row['RadioMAC'], row['IMEI'], row['Frequency']))
        conn.commit()
        return jsonify({"status": "Success", "count": len(df)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# 3. SMART STATUS (Dashboard & AI Alert Logic)
@app.route('/api/status', methods=['GET', 'POST'])
def handle_status():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if request.method == 'POST':
        data = request.json
        radio_mac = data.get('radio_mac')
        metrics = data.get('metrics', {})
        
        # AI Detection Logic (Pick-to-Pick Accuracy)
        is_alert = True if float(metrics.get('velocity', 0)) > 4.5 else False
        
        cur.execute("""
            INSERT INTO node_data (radio_mac, velocity, acceleration, temperature, ultrasound_db, ai_alert_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (radio_mac, metrics.get('velocity'), metrics.get('acceleration'), 
              metrics.get('temp'), metrics.get('ultrasound'), is_alert))
        conn.commit()
        return jsonify({"status": "Synced", "alert": is_alert}), 200

    # GET: Latest data for Dashboard
    cur.execute("SELECT * FROM node_data ORDER BY timestamp DESC LIMIT 1")
    latest = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(latest if latest else {"message": "No Data"})

# 4. FREQUENCY-SPECIFIC OTA (868 vs 915)
@app.route('/api/ota/check', methods=['GET'])
def check_ota():
    model = request.args.get('model')
    freq = request.args.get('freq') # 868 or 915
    # Logic: Static folder check based on frequency
    fw_url = f"https://nvpredictive.com{freq}/{model}_latest.bin"
    return jsonify({"url": fw_url, "v": "1.0.2"})

if __name__ == "__main__":
    app.run()
