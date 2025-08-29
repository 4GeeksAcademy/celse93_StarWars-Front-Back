from flask import request, jsonify
from models import db, Vehicles


def register_vehicles_routes(app):

    @app.route("/vehicles", methods=["GET", "POST"])
    def vehicles_collection():
        if request.method == "GET":
            vehicles = db.session.scalars(db.select(Vehicles)).all()
            result = [v.serialize() for v in vehicles]
            return jsonify(result)
        elif request.method == "POST":
            data = request.json
            vehicles = Vehicles(**data)
            db.session.add(vehicles)
            db.session.commit()
            result = vehicles.serialize()
            return jsonify(result), 201


    @app.route("/vehicles/<int:vehicle_id>", methods=["GET", "DELETE"])
    def vehicle_item(vehicle_id):
        vehicle = db.session.get(Vehicles, vehicle_id)
        if not vehicle:
            return {"error": "Vehicle not found"}, 404
        if request.method == "GET":
            result = vehicle.serialize()
            return jsonify(result)
        elif request.method == "DELETE":
            db.session.delete(vehicle)
            db.session.commit()
            return "", 204