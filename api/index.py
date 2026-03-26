# --- 1. USER & SITE MAPPING ---
@app.route('/api/admin/create-client', methods=['POST'])
def create_client():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password_hash, role, company_name, whatsapp_no) VALUES (%s, %s, 'client', %s, %s)", 
                    (data['email'], data['password'], data['company'], data['whatsapp']))
        conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/admin/site-map', methods=['POST'])
def site_mapping():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO site_node_mapping (user_id, radio_mac, site_name, motor_kw, rated_rpm, vib_limit_mm_s) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (radio_mac) DO UPDATE SET site_name = EXCLUDED.site_name", 
                    (data['uid'], data['mac'], data['site'], data['kw'], data['rpm'], data['limit']))
        conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e: return jsonify({"error": str(e)}), 500

# --- 2. DEVICE DETAILS ---
@app.route('/api/admin/device-details/<id>', methods=['GET'])
def device_details(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM device_inventory WHERE radio_mac=%s OR imei_id=%s", (id, id))
    device = cur.fetchone()
    return jsonify(device)
