from flask import Flask
from flasgger import Swagger
from app.modules.main.route import main_bp
from app.db.db import db


def initialize_route(app: Flask):
    with app.app_context():
        app.register_blueprint(main_bp, url_prefix='/api/v1/main')


def initialize_db(app: Flask):
    db.init_app(app)
    with app.app_context():
        import app.models
        db.create_all()

def initialize_swagger(app: Flask):
    with app.app_context():
        swagger = Swagger(app)
        return swagger