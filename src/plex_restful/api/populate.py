from ..plex.data import get_playlist_data
from .database import db
from .models import Playlist, PlaylistType, Track


def populate_db():
    try:
        db.create_all()

        # Define playlist types
        playlist_types = ["audio", "photo", "video"]
        created_playlist_types = {}
        for p_type in playlist_types:
            playlist_type_instance = PlaylistType(name=p_type)
            db.session.add(playlist_type_instance)
            created_playlist_types[p_type] = playlist_type_instance

        db.session.commit()

        # Fetch playlist data
        playlists_data = get_playlist_data()

        print("Fetched playlist data.")

        playlists = []
        tracks = []

        created_playlists = {}
        created_tracks = {}

        for playlist, tracks_list in playlists_data.items():
            print(f"Processing playlist: {playlist.title}")
            if playlist.title not in created_playlists:
                # Retrieve the corresponding PlaylistType instance
                playlist_type_instance = created_playlist_types.get(playlist.playlistType)
                print(
                    f"Playlist type for {playlist.title}: {playlist.playlistType} -> {playlist_type_instance}"
                )
                if not playlist_type_instance:
                    raise ValueError(f"Playlist type {playlist.playlistType} not found")
                print(f"Creating new playlist instance for: {playlist.title}")

                playlist_instance = Playlist(
                    title=playlist.title,
                    playlist_type=playlist_type_instance,  # Set the PlaylistType instance here
                    duration=playlist.duration,
                    thumb=playlist.thumb,
                )
                print(f"Playlist instance: {playlist_instance}")
                playlists.append(playlist_instance)
                created_playlists[playlist.title] = playlist_instance
            else:
                playlist_instance = created_playlists[playlist.title]

            for track in tracks_list:
                track_key = (track.title, track.trackNumber, track.parentTitle, track.grandparentTitle)
                if track_key not in created_tracks:
                    track_instance = Track(
                        title=track.title,
                        duration=track.duration,
                        track_number=track.trackNumber,
                        album=track.parentTitle,
                        artist=track.grandparentTitle,
                    )
                    # print(f"Creating new track instance for: {track.title}")
                    tracks.append(track_instance)
                    created_tracks[track_key] = track_instance
                else:
                    track_instance = created_tracks[track_key]

                playlist_instance.tracks.append(track_instance)

        print("Saving playlists and tracks to the database.")
        db.session.bulk_save_objects(playlists)
        db.session.bulk_save_objects(tracks)
        db.session.commit()
        print("Database commit successful.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
