from flask import Flask
from flask_cors import CORS

from .api.database import init_db
from .api.endpoints import api_bp
from .apps.default.routes import default_bp
from .config import DBConfig


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(DBConfig)

    # Initialize database
    init_db(app)

    # Register the blueprint with the app
    app.register_blueprint(default_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app


app = create_app()
