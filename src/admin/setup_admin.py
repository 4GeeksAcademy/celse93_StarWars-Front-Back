import os
from flask_admin import Admin
from models import db, Planets, Vehicles, Species, Characters
from admin.model_wrapper import StandardModelView


def setup_admin(app):
    app.secret_key = os.environ.get("FLASK_APP_KEY", "sample key")
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

    admin = Admin(app, name="4Geeks Admin", template_mode="bootstrap3")

    with app.app_context():
        admin.add_view(StandardModelView(Planets, db.session))
        admin.add_view(StandardModelView(Vehicles, db.session))
        admin.add_view(StandardModelView(Species, db.session))
        admin.add_view(StandardModelView(Characters, db.session))
