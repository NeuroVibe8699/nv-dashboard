from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import random

app = Flask(__name__)
CORS(app)

# Dummy Database (Testing ke liye)
inventory_db = [
    {"type": "Gateway", "mac": "GW-8699-01", "model": "NV-G1", "status": "Active"},
    {"type": "Node", "mac": "ND-8699-05", "model": "NV-V3", "status": "Pending"}
]

# 1. Export Logic (Excel file generate karega)
@app.route('/api/export-inventory', methods=['GET'])
def export_inv():
    df = pd.DataFrame(inventory_db)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventory')
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                     as_attachment=True, download_name='NeuroVibe_Inventory.xlsx')

# 2. Import Logic (Separate Columns for Gateway/Node)
@app.route('/api/import-inventory', methods=['POST'])
def import_inv():
    inv_type = request.form.get('type') # 'Gateway' or 'Node'
    file = request.files['file']
    # Logic: Excel read karke specific table mein save karna
    return jsonify({"status": "success", "message": f"{inv_type} Imported!"})

# 3. Discovery Logic (Agar MAC ID nahi pata)
@app.route('/api/discover', methods=['GET'])
def discover():
    # Network par jo naye devices mile hain (Random simulation)
    return jsonify([{"mac": "DISCOVERED-MAC-01"}, {"mac": "DISCOVERED-MAC-02"}])
