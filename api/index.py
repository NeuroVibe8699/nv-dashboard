import os
import pandas as pd
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# --- DATABASE CONNECTION ---
DB_URL = os.environ.get('POSTGRES_URL')

def get_db_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

# ---------------------------------------------------------
# 1. BULK INVENTORY IMPORT (Handles Node & Gateway Toggles)
# ---------------------------------------------------------
@app.route('/api/inventory/bulk-import', methods=['POST'])
def bulk_import():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    device_type = request.form.get('type') # 'node' or 'gateway' from admin.html toggle
    file = request.files['file']
    df = pd.read_excel(file) 
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        for _, row in df.iterrows():
            model = str(row['Model']).strip()
            # Frequency Logic: NVS-1001 (868), NVS-1002 (915) ... based on model ID
            freq = 915 if int(model.split('-')[-1]) % 2 == 0 else 868
            
            if device_type == 'node':
                cur.execute("""
                    INSERT INTO device_inventory (model_id, serial_no, radio_mac, ble_mac, rf_frequency, device_status)
                    VALUES (%s, %s, %s, %s, %s, 'factory_stock') 
                    ON CONFLICT (radio_mac) DO UPDATE SET ble_mac = EXCLUDED.ble_mac
                """, (model, row['Serial'], row['RadioMAC'], row.get('BLE_MAC'), freq))
            else:
                cur.execute("""
                    INSERT INTO device_inventory (model_id, serial_no, imei_id, radio_mac, lan_mac, wan_mac, rf_frequency, device_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'factory_stock') 
                    ON CONFLICT (imei_id) DO UPDATE SET lan_mac = EXCLUDED.lan_mac, wan_mac = EXCLUDED.wan_mac
                """, (model, row['Serial'], row['IMEI'], row.get('RadioMAC'), row.get('LAN'), row.get('WAN'), freq))
        
        conn.commit()
        return jsonify({"status": "Success", "message": f"Successfully imported {len(df)} {device_type}s"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# ---------------------------------------------------------
# 2. INVENTORY LIST (For Admin Dashboard Table)
# ---------------------------------------------------------
@app.route('/api/inventory/list', methods=['GET'])
def list_inventory():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_inventory ORDER BY registration_date DESC")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

# ---------------------------------------------------------
# 3. EXPORT INVENTORY (Download CSV)
# ---------------------------------------------------------
@app.route('/api/inventory/export', methods=['GET'])
def export_inventory():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM device_inventory", conn)
    conn.close()
    return df.to_csv(index=False), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=neurovibe_inventory.csv'
    }

# ---------------------------------------------------------
# 4. TELEMETRY & AI STATUS (Dashboard Data)
# ---------------------------------------------------------
@app.route('/api/status', methods=['GET', 'POST'])
def handle_status():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.json
        # Logic to save Node data (Velocity, Temp, etc.) into 'node_data' table
        # AI alert logic check here
        return jsonify({"status": "success"}), 200
    
    cur.execute("SELECT * FROM node_data ORDER BY timestamp DESC LIMIT 1")
    latest = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(latest if latest else {"metrics": {"velocity":0, "temp":0}})

if __name__ == "__main__":
    app.run()
