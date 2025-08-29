from flask import request, jsonify
from models import db, Characters
import requests  # pipenv install requests to instal package


def register_characters_routes(app):

    @app.route("/characters", methods=["GET", "POST"])
    def characters_collection():
        response_body = {}
        if request.method == "GET":
            url = 'https://swapi.info/api/people'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                response_body = data

            return response_body, 200

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
                url = f'https://swapi.info/api/people/{character_id}'
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    # Check if charact exisits in DB
                    existing_char = db.session.scalar(
                        db.select(Characters).filter_by(id=character_id))

                    if not existing_char:
                        # get ID from url of homeworld property's value
                        planet_id = int(data["homeworld"].split("/")[-1])

                        if len(data["species"]) != 0:
                            specie_id = int(data["species"][0].split("/")[-1])
                        else:
                            specie_id = None

                        # Create new charac if its not in DB
                        char = Characters(
                            id=int(character_id),
                            name=data["name"],
                            birth_year=data["birth_year"],
                            gender=data["gender"],
                            planet_id=planet_id,
                            specie_id=specie_id
                        )
                        db.session.add(char)
                        db.session.commit()
                    else:
                        # Get charac if its in DB
                        char = existing_char

                    # Serialize charac objet.
                    response_body['results'] = char.serialize()
                else:
                    response_body[
                        'error'] = f'Error retrieving SWAPI data. Code status: {response.status_code}'

                return response_body, 200

            else:
                result = character.serialize()
                return jsonify(result)

        elif request.method == "DELETE":
            delete_char = db.session.scalar(
                db.select(Characters).filter_by(id=character_id))

            if not delete_char:
                response_body['message'] = f'The character with ID:{character_id} wasnt found.'
                return response_body, 404
            else:
                db.session.delete(delete_char)
                db.session.commit()
                response_body['message'] = f'Character ID:{character_id} was deleted.'
                response_body['results'] = {}

            return response_body, 204
