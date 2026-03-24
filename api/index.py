@app.route('/api/latest-data', methods=['GET'])
def latest_data():
    # Yahan Database query (SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1) aayegi
    return jsonify({
        "velocity": 1.42,
        "acceleration": 0.07,
        "temperature": 45.6,
        "rpm": 1445,
        "flux": 92,
        "ultrasound": 15.1
    })
