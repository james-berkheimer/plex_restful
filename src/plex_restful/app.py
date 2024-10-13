from flask import Flask
from flask_cors import CORS

from .api.endpoints import api_bp
from .apps.refresh.routes import main
from .config import DBConfig, ServerConfig, SocketioConfig

socketio = SocketioConfig.socketio


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(DBConfig)

    app.register_blueprint(main)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app


app = create_app()
if __name__ == "__main__":
    socketio.run(app, host=ServerConfig.HOST, port=ServerConfig.PORT, debug=ServerConfig.DEBUG)
