from flask import request, jsonify
from models import db, Species


def register_species_routes(app):

    @app.route("/species", methods=["GET", "POST"])
    def species_collection():
        if request.method == "GET":
            species = db.session.scalars(db.select(Species)).all()
            result = [s.serialize() for s in species]
            return jsonify(result)
        elif request.method == "POST":
            data = request.json
            species = Species(**data)
            db.session.add(species)
            db.session.commit()
            result = species.serialize()
            return jsonify(result), 201


    @app.route("/species/<int:specie_id>", methods=["GET", "DELETE"])
    def specie_item(specie_id):
        specie = db.session.get(Species, specie_id)
        if not specie:
            return {"error": "Specie not found"}, 404
        if request.method == "GET":
            result = specie.serialize()
            return jsonify(result)
        elif request.method == "DELETE":
            db.session.delete(specie)
            db.session.commit()
            return "", 204