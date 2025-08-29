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
                            id= planet_id,
                            name= planet["name"],
                            climate= planet["climate"],
                            population= planet["population"]
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
        planet = db.session.get(Planets, planet_id)
        if not planet:
            return {"error": "Planet not found"}, 404
        if request.method == "GET":
            result = planet.serialize()
            return jsonify(result)
        elif request.method == "DELETE":
            db.session.delete(planet)
            db.session.commit()
            return "", 204