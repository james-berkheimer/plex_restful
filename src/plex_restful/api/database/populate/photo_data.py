"""
playlists = plex_server.playlists()
for playlist in playlists:
    if playlist.title == "Charity":
        for photo in playlist.items():
            print(photo.title)
            media = photo.media
            if len(media) == 1:
                print(media[0].parts[0].file)
            else:
                print("Multiple media")
"""

from ....plex.data import get_playlist_data
from ...extensions import db
from ..models import Photo, Playlist


def populate_photo_data():
    try:
        # Fetch playlist data
        print("Fetching playlist data...")
        playlists_data = get_playlist_data()

    except Exception as e:
        print(f"Error populating photo data: {str(e)}")
        db.session.rollback()
        raise e
    finally:
        db.session.close()
