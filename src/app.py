"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from sqlalchemy import select
from models import db, User, Favorite, Character, Vehicle, Planet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_user():
    users = db.session.scalars(select(User)).all()
    users_dictionaries = []
    for user in users:
        users_dictionaries.append(
            user.serialize()
        )
    return jsonify(users_dictionaries), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = db.session.scalars(select(Character)).all()
    characters_dictionaries = []
    for character in characters:
        characters_dictionaries.append(
            character.serialize()
        )
    return jsonify(characters_dictionaries), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = db.session.scalars(select(Planet)).all()
    planets_dictionaries = []
    for planet in planets:
        planets_dictionaries.append(
            planet.serialize()
        )
    return jsonify(planets_dictionaries), 200


@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = db.session.scalars(select(Vehicle)).all()
    vehicles_dictionaries = []
    for vehicle in vehicles:
        vehicles_dictionaries.append(
            vehicle.serialize()
        )
    return jsonify(vehicles_dictionaries), 200


# These two lines should always be at the end of your app.py file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)
