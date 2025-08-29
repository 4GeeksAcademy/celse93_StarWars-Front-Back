from flask import request, jsonify
from models import db, Post, Comment, Media


def register_post_routes(app):

    @app.route("/posts", methods=["GET", "POST"])
    def posts_collection():
        if request.method == "GET":
            posts = db.session.scalars(db.select(Post)).all()
            result = [p.serialize() for p in posts]
            return jsonify(result)
        elif request.method == "POST":
            data = request.json
            post = Post(**data)
            db.session.add(post)
            db.session.commit()
            result = post.serialize()
            return jsonify(result), 201

    @app.route("/posts/<int:post_id>", methods=["GET", "DELETE"])
    def post_item(post_id):
        post = db.session.get(Post, post_id)
        if not post:
            return {"error": "Post not found"}, 404
        if request.method == "GET":
            result = post.serialize()
            return jsonify(result)
        elif request.method == "DELETE":
            db.session.delete(post)
            db.session.commit()
            return "", 204

    @app.route("/posts/<int:post_id>/comments", methods=["GET"])
    def post_comments(post_id):
        comments = db.session.scalars(
            db.select(Comment).filter_by(post_id=post_id)
        ).all()
        result = [c.serialize() for c in comments]
        return jsonify(result)

    @app.route("/posts/<int:post_id>/media", methods=["GET"])
    def post_media(post_id):
        media_items = db.session.scalars(
            db.select(Media).filter_by(post_id=post_id)
        ).all()
        result = [m.serialize() for m in media_items]
        return jsonify(result)
