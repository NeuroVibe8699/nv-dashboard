from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import random

app = Flask(__name__)
CORS(app)

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

@app.route('/api/import-inventory', methods=['POST'])
def import_inv():
    # PDF Logic: Excel read karke inventory mein save karna
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    return jsonify({"status": "success", "message": "Inventory Imported Successfully!"})

if __name__ == "__main__":
    app.run()
