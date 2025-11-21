from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Jeu de données de test, comme si tu recevais du capteur
sensor_data = {
    "temperature": 23.7,
    "humidity": 58,
    "light": 340,
    "air_quality": 105,
    "timestamp": datetime.now().isoformat()
}

@app.route('/api/latest', methods=['GET'])
def get_latest():
    return jsonify(sensor_data)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
