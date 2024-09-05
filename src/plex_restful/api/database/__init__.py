import time

from ..extensions import db
from .populate import populate_database


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # populate_db()
        start_time = time.time()
        populate_database()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"populate_db function executed in {elapsed_time:.2f} seconds")
