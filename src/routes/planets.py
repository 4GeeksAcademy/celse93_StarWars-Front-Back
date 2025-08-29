from flask import request, jsonify
from models import db, Planets


def register_planets_routes(app):

    @app.route("/planets", methods=["GET", "POST"])
    def planets_collection():
        if request.method == "GET":
            planets = db.session.scalars(db.select(Planets)).all()
            result = [p.serialize() for p in planets]
            return jsonify(result)
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