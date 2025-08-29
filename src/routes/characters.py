from flask import request, jsonify
from models import db, Characters


def register_characters_routes(app):

    @app.route("/characters", methods=["GET", "POST"])
    def characters_collection():
        if request.method == "GET":
            characters = db.session.scalars(db.select(Characters)).all()
            result = [c.serialize() for c in characters]
            return jsonify(result)
        elif request.method == "POST":
            data = request.json
            characters = Characters(**data)
            db.session.add(characters)
            db.session.commit()
            result = characters.serialize()
            return jsonify(result), 201


    @app.route("/characters/<int:character_id>", methods=["GET", "DELETE"])
    def character_item(character_id):
        character = db.session.get(Characters, character_id)
        if not character:
            return {"error": "Character not found"}, 404
        if request.method == "GET":
            result = character.serialize()
            return jsonify(result)
        elif request.method == "DELETE":
            db.session.delete(character)
            db.session.commit()
            return "", 204