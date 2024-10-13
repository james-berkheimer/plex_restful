import os

from flask_socketio import SocketIO


class DBConfig:
    DB_PATH = "sqlite:///src/instance/plex_restful.db"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///plex_restful.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class PlexConfig:
    # CRED_PATH = "/home/james/code/plex_restful/tests/.plex_cred"
    CRED_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tests/.plex_cred/credentials.json"
    )


class ServerConfig:
    HOST = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_RUN_PORT", 5090))
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"


class SocketioConfig:
    socketio = SocketIO()
