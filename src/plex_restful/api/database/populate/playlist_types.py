from ...extensions import db
from ..models import PlaylistType


def populate_playlist_types():
    print("Defining playlist types...")
    playlist_types = ["audio", "photo", "video"]
    existing_playlist_types = {ptype.name: ptype for ptype in PlaylistType.query.all()}

    for p_type in playlist_types:
        if p_type not in existing_playlist_types:
            playlist_type_instance = PlaylistType(name=p_type)
            db.session.add(playlist_type_instance)
            existing_playlist_types[p_type] = playlist_type_instance
    db.session.commit()
    print("Playlist types committed to database.")
