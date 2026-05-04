from flask import Flask
import os
from flask_apscheduler import APScheduler
from app.config.config import DevelopmentConfig, TestingConfig
from app.initialize_functions import initialize_route, initialize_db, initialize_swagger
from app.admin import setup_admin
from flask_jwt_extended import JWTManager
from app.seed_data import run_seed
from app.modules.patient.dao import auto_cancel_unpaid

scheduler = APScheduler()
def create_app(config_name="development") -> Flask:
    flask_app = Flask(__name__)
    if config_name == "testing":
        flask_app.config.from_object(TestingConfig)
    else:
        flask_app.config.from_object(DevelopmentConfig)
        scheduler.init_app(flask_app)
        

        def scheduled_auto_cancel():
            with flask_app.app_context():
                auto_cancel_unpaid()

        scheduler.add_job(
            id="auto_cancel_unpaid",
            func=scheduled_auto_cancel,
            trigger="interval",
            minutes=5,
            replace_existing=True
        )

        scheduler.start()

    jwt = JWTManager(flask_app)
    # Initialize extensions
    initialize_db(flask_app)

    # Register blueprints
    initialize_route(flask_app)

    # Initialize Swagger
    initialize_swagger(flask_app)

    # Setup admin interface
    setup_admin(flask_app)

    @flask_app.cli.command("seed")
    def seed():
        run_seed()

    return flask_app