import os
import pandas as pd
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# Database Connection (Vercel Postgres)
DB_URL = os.environ.get('POSTGRES_URL')

def get_db_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

# --- 1. LOGIN SYSTEM (Smart Redirect) ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    u, p = data.get('u'), data.get('p')
    
    if u == "admin@nvpredictive.com" and p == "admin123":
        return jsonify({"status": "success", "role": "admin", "redirect": "/admin.html"}), 200
        
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM users WHERE username=%s AND password_hash=%s", (u, p))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return jsonify({"status": "success", "role": "client", "redirect": "/dashboard.html", "uid": user['id']}), 200
    except: pass
    
    return jsonify({"status": "error", "message": "Invalid Credentials"}), 401

# --- 2. INVENTORY (Bulk Import with Frequency Logic) ---
@app.route('/api/inventory/bulk-import', methods=['POST'])
def bulk_import():
    try:
        device_type = request.form.get('type')
        file = request.files['file']
        df = pd.read_excel(file)
        conn = get_db_connection()
        cur = conn.cursor()
        for _, row in df.iterrows():
            model = str(row['Model']).strip()
            freq = 915 if int(model.split('-')[-1]) % 2 == 0 else 868
            if device_type == 'node':
                cur.execute("INSERT INTO device_inventory (model_id, serial_no, radio_mac, ble_mac, rf_frequency) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (radio_mac) DO NOTHING", (model, row['Serial'], row['RadioMAC'], row.get('BLE_MAC'), freq))
            else:
                cur.execute("INSERT INTO device_inventory (model_id, serial_no, imei_id, radio_mac, lan_mac, wan_mac, rf_frequency) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (imei_id) DO NOTHING", (model, row['Serial'], row['IMEI'], row.get('RadioMAC'), row.get('LAN'), row.get('WAN'), freq))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "message": f"{len(df)} Devices Added"}), 200
    except Exception as e: return jsonify({"status": "error", "message": str(e)}), 500

# --- 3. MAPPING HELPERS (Dropdown Data) ---
@app.route('/api/admin/get-mapping-data', methods=['GET'])
def get_mapping_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, company_name FROM users WHERE role='client'")
    users = cur.fetchall()
    cur.execute("SELECT radio_mac FROM device_inventory WHERE radio_mac IS NOT NULL")
    nodes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"users": users, "nodes": nodes})

# --- 4. SITE MAPPING & USER CREATE ---
@app.route('/api/admin/create-client', methods=['POST'])
def create_client():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash, role, company_name, whatsapp_no) VALUES (%s, %s, 'client', %s, %s)", (data['email'], data['password'], data['company'], data['whatsapp']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"}), 200

@app.route('/api/admin/site-map', methods=['POST'])
def site_mapping():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO site_node_mapping (user_id, radio_mac, site_name, rated_rpm, vib_limit_mm_s) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (radio_mac) DO UPDATE SET site_name = EXCLUDED.site_name", (data['uid'], data['mac'], data['site'], data['rpm'], data['limit']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"}), 200

# --- 5. TELEMETRY STATUS (Live Data) ---
@app.route('/api/status', methods=['GET'])
def get_node_status():
    mac = request.args.get('radio_mac')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM node_data WHERE radio_mac=%s ORDER BY timestamp DESC LIMIT 1", (mac,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(data if data else {"message": "No data found"})

@app.route('/api/inventory/list', methods=['GET'])
def list_inventory():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_inventory ORDER BY registration_date DESC")
    return jsonify(cur.fetchall())

if __name__ == "__main__":
    app.run()
