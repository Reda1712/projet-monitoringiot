# projet-monitoringiot

## Objectif
Collecter et visualiser des mesures environnementales IoT (température, humidité, luminosité, qualité d’air).

## Matériel et capteurs
- Arduino UNO + DHT22, LDR, MQ135
- Câbles, breadboard

## Installation rapide
1. Crée un environnement virtuel :
   python3 -m venv venv
   source venv/bin/activate
2. Installe les dépendances :
   pip install -r requirements.txt
3. Lance le serveur :
   python app.py

## API disponibles
- POST /api/add : ajoute une mesure
- GET /api/history : historique complet
- GET /api/latest : dernière mesure
- GET /dashboard : tableau web
- GET /api/filter?min_temp=22&max_temp=28 : filtrage avancé

## Exemples
curl "http://127.0.0.1:5000/api/history"
curl "http://127.0.0.1:5000/api/filter?min_temp=24"

## (Facultatif) Capture d’écran ou schéma
Ajoute une image illustrant le dashboard web ou le schéma des capteurs.

## Idées bonus
- Ajouter des graphiques
- Notifications en cas de seuil critique
