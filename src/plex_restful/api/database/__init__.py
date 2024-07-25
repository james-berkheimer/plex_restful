import time

from ..extensions import db
from .populate.audio_data import populate_audio_data
from .populate.playlist_types import populate_playlist_types


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        populate_db()


def populate_db():
    start_time = time.time()
    populate_playlist_types()
    populate_audio_data()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"populate_db function executed in {elapsed_time:.2f} seconds")
