import os
import pandas as pd
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# Database Connection
DB_URL = os.environ.get('POSTGRES_URL')

def get_db_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

# 1. AUTHENTICATION (Login Fix)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    u = data.get('u')
    p = data.get('p')
    
    # Master Credentials
    if u == "admin@nvpredictive.com" and p == "admin123":
        return jsonify({"status": "success", "role": "admin"}), 200
    return jsonify({"status": "error", "message": "Invalid Credentials"}), 401

# 2. BULK INVENTORY IMPORT (Node/Gateway Toggle Logic)
@app.route('/api/inventory/bulk-import', methods=['POST'])
def bulk_import():
    try:
        device_type = request.form.get('type') # 'node' or 'gateway'
        file = request.files['file']
        df = pd.read_excel(file)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        for _, row in df.iterrows():
            model = str(row['Model']).strip()
            # Freq: Odd = 868, Even = 915
            freq = 915 if int(model.split('-')[-1]) % 2 == 0 else 868
            
            if device_type == 'node':
                cur.execute("""
                    INSERT INTO device_inventory (model_id, serial_no, radio_mac, ble_mac, rf_frequency)
                    VALUES (%s, %s, %s, %s, %s) ON CONFLICT (radio_mac) DO NOTHING
                """, (model, row['Serial'], row['RadioMAC'], row.get('BLE_MAC'), freq))
            else:
                cur.execute("""
                    INSERT INTO device_inventory (model_id, serial_no, imei_id, radio_mac, lan_mac, wan_mac, rf_frequency)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (imei_id) DO NOTHING
                """, (model, row['Serial'], row['IMEI'], row.get('RadioMAC'), row.get('LAN'), row.get('WAN'), freq))
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "message": f"{len(df)} Devices Imported"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 3. INVENTORY LIST
@app.route('/api/inventory/list', methods=['GET'])
def list_inventory():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_inventory ORDER BY registration_date DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run()
