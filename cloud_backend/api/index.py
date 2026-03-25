from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import random

app = Flask(__name__)
CORS(app)

# 1. Live Data (Har 1.5 sec mein change hoga)
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "metrics": {
            "velocity": round(random.uniform(3.5, 4.5), 2),
            "acceleration": round(random.uniform(0.8, 1.2), 2),
            "temp": round(random.uniform(38.0, 42.0), 1),
            "flux": round(random.uniform(0.09, 0.11), 3),
            "rpm": random.randint(1440, 1480),
            "ultrasound": round(random.uniform(25.0, 30.0), 1)
        },
        "spectrum": [random.uniform(2, 10) for _ in range(30)]
    })

# 2. Dynamic Token Generator (Har baar naya number aayega)
@app.route('/api/get-token', methods=['GET'])
def get_token():
    new_token = f"NV-{random.randint(100000, 999999)}"
    return jsonify({"token": new_token})

# 3. Excel Export Logic
@app.route('/api/export', methods=['GET'])
def export_inv():
    data = [{"Type": "Gateway", "MAC": "GW-NV-01", "Status": "Active"}, {"Type": "Node", "MAC": "ND-NV-05", "Status": "Active"}]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='NeuroVibe_Inventory.xlsx')
