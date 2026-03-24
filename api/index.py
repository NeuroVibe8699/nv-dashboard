from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/status', methods=['GET'])
def get_status():
    # PDF Ref 0.1.2: Real-time values simulation
    return jsonify({
        "status": "Online",
        "metrics": {
            "velocity": round(random.uniform(2.5, 5.0), 2),
            "acceleration": round(random.uniform(0.8, 1.4), 2),
            "temp": round(random.uniform(38, 45), 1),
            "flux": round(random.uniform(0.08, 0.12), 3),
            "rpm": random.randint(1440, 1490),
            "ultrasound": round(random.uniform(22, 35), 1)
        },
        "spectrum": [random.uniform(1, 10) for _ in range(30)]
    })

# Vercel handler
def handler(request):
    return app(request)

# Vercel ke liye expose karna zaroori hai
app = app
