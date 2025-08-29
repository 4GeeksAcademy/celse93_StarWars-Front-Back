from flask import request, jsonify
from models import db, Characters
import requests  # pipenv install requests to instal package


def register_characters_routes(app):

    @app.route("/characters", methods=["GET", "POST"])
    def characters_collection():
        response_body = {}
        if request.method == "GET":
            # Check if characters exists in DB
            characters = db.session.scalars(db.select(Characters)).all()

            if not characters:
                url = 'https://swapi.info/api/people'
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    for charac in data:
                        # get IDs from data properties' url value
                        character_id = int(charac["url"].split("/")[-1])
                        planet_id = int(charac["homeworld"].split("/")[-1])
                        if len(charac["species"]) != 0:
                            specie_id = int(
                                charac["species"][0].split("/")[-1])
                        else:
                            specie_id = None
                        # Add characters if not in DB
                        db.session.add(Characters(
                            id=int(character_id),
                            name=charac["name"],
                            birth_year=charac["birth_year"],
                            gender=charac["gender"],
                            planet_id=planet_id,
                            specie_id=specie_id
                        ))
                    db.session.commit()
                    characters = db.session.scalars(
                        db.select(Characters)).all()
                    # Serialize characters objet.
                    response_body = [c.serialize() for c in characters]
                    return jsonify(response_body), 201
                else:
                    response_body[
                        'error'] = f'Error retrieving SWAPI data. Code status: {response.status_code}'
                    return response_body
            else:
                # Get charac if its in DB + serialize characters objet
                response_body = [c.serialize() for c in characters]
                return jsonify(response_body), 200

        elif request.method == "POST":
            data = request.json
            characters = Characters(**data)
            db.session.add(characters)
            db.session.commit()
            result = characters.serialize()
            return jsonify(result), 201

    @app.route("/characters/<int:character_id>", methods=["GET", "DELETE"])
    def character_item(character_id):
        response_body = {}
        if request.method == "GET":
            character = db.session.get(Characters, character_id)

            if not character:
                response_body[
                    'error'] = f'Character ID:{character_id} doesnt exist.'
            else:
                response_body["result"] = character.serialize()

            return jsonify(response_body), 200

        elif request.method == "DELETE":
            delete_char = db.session.scalar(
                db.select(Characters).filter_by(id=character_id))

            if not delete_char:
                response_body['message'] = f'Character ID:{character_id} wasnt found.'
                return response_body, 404
            else:
                db.session.delete(delete_char)
                db.session.commit()
                response_body['message'] = f'Character ID:{character_id} was deleted.'
                response_body['results'] = {}

            return response_body, 204
