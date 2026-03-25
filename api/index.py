from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import random

app = Flask(__name__)
CORS(app)

# 1. Dashboard Metrics Logic
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "metrics": {"velocity": 4.12, "acceleration": 0.98, "temp": 42.5, "flux": 0.10, "rpm": 1450, "ultrasound": 26.8},
        "spectrum": [random.uniform(2, 12) for _ in range(30)]
    })

# 2. Discovery Logic (Agar MAC ID nahi pata - PDF Page 3)
@app.route('/api/discover', methods=['GET'])
def discover():
    return jsonify([{"mac": "NV-GW-99-A1"}, {"mac": "NV-ND-05-B2"}])

# 3. Export Logic (As per your request)
@app.route('/api/export', methods=['GET'])
def export_data():
    data = [{"Type": "Gateway", "MAC": "GW-01", "Status": "Active"}, {"Type": "Node", "MAC": "ND-05", "Status": "Active"}]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='NeuroVibe_Inventory.xlsx')

if __name__ == "__main__":
    app.run()
