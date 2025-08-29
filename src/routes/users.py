from flask import request, jsonify
from models import db, User, Follower, Post


def register_user_routes(app):

    @app.route("/users", methods=["GET", "POST"])
    def users_collection():
        if request.method == "GET":
            users = db.session.scalars(db.select(User)).all()
            result = [u.serialize() for u in users]
            return jsonify(result)
        elif request.method == "POST":
            data = request.json
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            result = user.serialize()
            return jsonify(result), 201

    @app.route("/users/<int:user_id>", methods=["GET", "DELETE"])
    def user_item(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return {"error": "User not found"}, 404
        if request.method == "GET":
            result = user.serialize()
            return jsonify(result)
        elif request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()
            return "", 204

    @app.route("/users/<int:user_id>/posts", methods=["GET"])
    def user_posts(user_id):
        posts = db.session.scalars(
            db.select(Post).filter_by(user_id=user_id)
        ).all()
        result = [p.serialize() for p in posts]
        return jsonify(result)

    @app.route("/followers", methods=["POST", "DELETE"])
    def followers_collection():
        data = request.json
        if request.method == "POST":
            follower = Follower(**data)
            db.session.add(follower)
            db.session.commit()
            result = follower.serialize()
            return jsonify(result), 201
        elif request.method == "DELETE":
            follower = db.session.get(
                Follower, (data["user_from_id"], data["user_to_id"])
            )
            if not follower:
                return {"error": "Not found"}, 404
            db.session.delete(follower)
            db.session.commit()
            return "", 204
