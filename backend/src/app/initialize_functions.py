from flask import Flask
from flasgger import Swagger
from app.db.db import db
from app.modules.patient.routes import patient_bp
from app.modules.doctor.routes import doctor_bp
from app.modules.user.routes import auth_bp
from app.modules.web.routes import web_bp
from app.modules.menu_bar.routes import menu_bp
from flask_migrate import Migrate

def initialize_route(app: Flask):
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(web_bp)
    app.register_blueprint(menu_bp, url_prefix='/api/menu')

# migrate = Migrate()
def initialize_db(app: Flask):
    db.init_app(app)
    if not app.config.get("TESTING"):
        migrate = Migrate()
        migrate.init_app(app, db)

    with app.app_context():
        import app.models

def initialize_swagger(app: Flask):
    if not app.config.get("TESTING"):
        with app.app_context():
            swagger = Swagger(app)
            return swagger
    return None