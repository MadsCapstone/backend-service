"""Flask app initialization via factory pattern."""
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow

from backend_api.config import get_config

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
# ma = Marshmallow()

def create_app(config_name):
    app = Flask("backend_api")
    app_config = get_config(config_name)
    app.config.from_object(app_config)

    from backend_api.api import api_bp
    app.register_blueprint(api_bp)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, directory=app_config.MIGRATIONS_FOLDER)
    bcrypt.init_app(app)
    # ma.init_app(app)
    return app