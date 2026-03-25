from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# 1. Live Status Logic
@app.route('/api/status', methods=['GET'])
def get_status():
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

# 2. Dynamic Token Logic (Har Gateway ke liye alag)
@app.route('/api/generate-token', methods=['GET'])
def generate_token():
    # Naya unique 6-digit token
    new_token = f"NV-{random.randint(100000, 999999)}"
    return jsonify({"token": new_token})

if __name__ == "__main__":
    app.run()
