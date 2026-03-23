from flask import Flask
from app.config.config import DevelopmentConfig
from app.initialize_functions import initialize_route, initialize_db, initialize_swagger
from app.admin import setup_admin

def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    initialize_db(flask_app)

    # Register blueprints
    initialize_route(flask_app)

    # Initialize Swagger
    initialize_swagger(flask_app)

    # Setup admin interface
    setup_admin(flask_app)

    return flask_app
