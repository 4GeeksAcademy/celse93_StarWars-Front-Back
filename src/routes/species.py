from flask import request, jsonify
from models import db, Species
import requests


def register_species_routes(app):

    @app.route("/species", methods=["GET", "POST"])
    def species_collection():
        response_body = {}
        if request.method == "GET":
            species = db.session.scalars(db.select(Species)).all()

            if not species:
                url = 'https://swapi.info/api/species'
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()

                    for specie in data:
                        specie_id = int(specie["url"].split("/")[-1])
                        db.session.add(Species(
                            id=specie_id,
                            name=specie["name"],
                            designation=specie["designation"],
                            language=specie["language"]
                        ))
                    db.session.commit()
                    species = db.session.scalars(db.select(Species)).all()
                    response_body = [s.serialize() for s in species]
                    return jsonify(response_body), 201
                else:
                    response_body[
                        'error'] = f'Error retrieving SWAPI data. Code status: {response.status_code}'
                    return response_body
            else:
                response_body = [s.serialize() for s in species]
                return jsonify(response_body), 200

        elif request.method == "POST":
            data = request.json
            species = Species(**data)
            db.session.add(species)
            db.session.commit()
            result = species.serialize()
            return jsonify(result), 201

    @app.route("/species/<int:specie_id>", methods=["GET", "DELETE"])
    def specie_item(specie_id):
        response_body = {}
        if request.method == "GET":
            specie = db.session.get(Species, specie_id)
            if not specie:
                response_body[
                    'error'] = f'Specie ID:{specie_id} doesnt exist.'
            else:
                response_body["result"] = specie.serialize()
            return jsonify(response_body), 200

        elif request.method == "DELETE":
            delete_specie = db.session.scalar(
                db.select(Species).filter_by(id=specie_id))
            if not delete_specie:
                response_body['message'] = f'Specie ID:{specie_id} wasnt found.'
                return response_body, 404
            else:
                db.session.delete(delete_specie)
                db.session.commit()
                response_body['message'] = f'Specie ID:{specie_id} was deleted.'
                response_body['results'] = {}
            return response_body, 204
