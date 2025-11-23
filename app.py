from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request

app = Flask(__name__)
CORS(app)

# Configuration de la base SQLite.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Définition du modèle de données du capteur
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    light = db.Column(db.Integer)
    air_quality = db.Column(db.Integer)
    timestamp = db.Column(db.String(100))

# Route pour ajouter une mesure capteur (depuis frontend ou capteur)
@app.route('/api/add', methods=['POST'])
def add_data():
    data = request.get_json()
    new_entry = SensorData(
        temperature=data['temperature'],
        humidity=data['humidity'],
        light=data['light'],
        air_quality=data['air_quality'],
        timestamp=data['timestamp']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Data saved!"}), 201

# Route pour consulter tout l’historique des mesures
@app.route('/api/history', methods=['GET'])
def get_history():
    all_data = SensorData.query.all()
    result = [
        {
            "temperature": entry.temperature,
            "humidity": entry.humidity,
            "light": entry.light,
            "air_quality": entry.air_quality,
            "timestamp": entry.timestamp
        }
        for entry in all_data
    ]
    return jsonify(result), 200

@app.route('/dashboard')
def dashboard():
    all_data = SensorData.query.all()
    return render_template('dashboard.html', data=all_data)

@app.route('/api/filter', methods=['GET'])
def filter_data():
    min_temp = request.args.get('min_temp')
    max_temp = request.args.get('max_temp')
    filtered = SensorData.query
    if min_temp:
        filtered = filtered.filter(SensorData.temperature >= float(min_temp))
    if max_temp:
        filtered = filtered.filter(SensorData.temperature <= float(max_temp))
    results = filtered.all()
    data = [
        {
            "temperature": entry.temperature,
            "humidity": entry.humidity,
            "light": entry.light,
            "air_quality": entry.air_quality,
            "timestamp": entry.timestamp
        }
        for entry in results
    ]
    return jsonify(data), 200

# Route pour vérifier la santé du serveur
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/api/latest', methods=['GET'])
def get_latest():
    latest_entry = SensorData.query.order_by(SensorData.id.desc()).first()
    if latest_entry:
        data = {
            "temperature": latest_entry.temperature,
            "humidity": latest_entry.humidity,
            "light": latest_entry.light,
            "air_quality": latest_entry.air_quality,
            "timestamp": latest_entry.timestamp
        }
        return jsonify(data), 200
    else:
        return jsonify({"error": "No data available"}), 404

