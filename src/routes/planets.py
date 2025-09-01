from flask import request, jsonify
from models import db, Planets
import requests


def register_planets_routes(app):

    @app.route("/planets", methods=["GET", "POST"])
    def planets_collection():
        response_body = {}
        if request.method == "GET":
            planets = db.session.scalars(db.select(Planets)).all()

            if not planets:
                url = 'https://swapi.info/api/planets'
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()

                    for planet in data:
                        planet_id = int(planet["url"].split("/")[-1])
                        db.session.add(Planets(
                            id=planet_id,
                            name=planet["name"],
                            climate=planet["climate"],
                            population=planet["population"]
                        ))
                    db.session.commit()
                    planets = db.session.scalars(db.select(Planets)).all()
                    response_body = [p.serialize() for p in planets]
                    return jsonify(response_body), 201
                else:
                    response_body[
                        'error'] = f'Error retrieving SWAPI data. Code status: {response.status_code}'
                    return response_body

            else:
                response_body = [p.serialize() for p in planets]
                return jsonify(response_body), 200

        elif request.method == "POST":
            data = request.json
            planets = Planets(**data)
            db.session.add(planets)
            db.session.commit()
            result = planets.serialize()
            return jsonify(result), 201

    @app.route("/planets/<int:planet_id>", methods=["GET", "DELETE"])
    def planet_item(planet_id):
        response_body = {}
        if request.method == "GET":
            planet = db.session.get(Planets, planet_id)
            if not planet:
                response_body['error'] = f'Planet ID:{planet_id} doesnt exist.'
            else:
                response_body["result"] = planet.serialize()
            return jsonify(response_body), 200

        elif request.method == "DELETE":
            delete_planet = db.session.scalar(
                db.select(Planets).filter_by(id=planet_id))
            if not delete_planet:
                response_body['message'] = f'Specie ID:{planet_id} wasnt found.'
                return response_body, 404
            else:
                db.session.delete(delete_planet)
                db.session.commit()
                response_body['message'] = f'Specie ID:{planet_id} was deleted.'
                response_body['results'] = {}
            return response_body, 204
