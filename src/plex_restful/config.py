import os


class DBConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///plex_restful.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
