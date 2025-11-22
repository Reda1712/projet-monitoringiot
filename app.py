from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

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

# Route pour vérifier la santé du serveur
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


