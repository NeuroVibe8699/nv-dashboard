from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import io
import random

app = Flask(__name__)
CORS(app)

# 1. Live Data (Dashboard)
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
        }
    })

# 2. Export Inventory (Excel Logic)
@app.route('/api/export', methods=['GET'])
def export_inv():
    # PDF Logic: Gateway aur Node ka consolidated data
    data = [{"Type": "Gateway", "MAC": "GW-8699-01", "Model": "NV-G1"}, {"Type": "Node", "MAC": "ND-05", "Model": "NV-V3"}]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='NV_Inventory.xlsx')

# 3. Discovery Mode (Agar MAC ID nahi pata)
@app.route('/api/discover', methods=['GET'])
def discover():
    return jsonify([{"mac": "NV-DISCOVER-01"}, {"mac": "NV-DISCOVER-02"}])

if __name__ == "__main__":
    app.run()
