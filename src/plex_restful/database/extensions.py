from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from ..config import DBConfig


# Define the base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Initialize Flask extensions
db = SQLAlchemy(model_class=Base)

# Database configuration
# db_path = "sqlite:///src/instance/plex_restful.db"
db_path = DBConfig.DB_PATH

# Create an engine and connect to the database
engine = create_engine(db_path)

# Reflect the database schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
