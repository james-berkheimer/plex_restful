from ....plex.data import get_playlist_data
from ...extensions import db
from ..models import Album, Artist, Playlist, PlaylistType, Track


def populate_audio_data():
    try:
        # Fetch playlist types
        existing_playlist_types = {ptype.name: ptype for ptype in PlaylistType.query.all()}

        # Fetch playlist data
        print("Fetching playlist data...")
        playlists_data = get_playlist_data()

        # Pre-fetch existing data
        existing_playlists = {p.title: p for p in Playlist.query.all()}
        existing_tracks = {
            (t.title, t.track_number, t.album_title, t.artist_name): t for t in Track.query.all()
        }
        existing_albums = {a.title: a for a in Album.query.all()}
        existing_artists = {a.name: a for a in Artist.query.all()}

        playlists = []
        tracks = []
        albums = []
        artists = []
        playlist_track_associations = []
        album_artist_associations = []

        print("Creating instances for playlists, tracks, albums, and artists...")
        for playlist, tracks_list in playlists_data.items():
            # Create Playlist instances
            if playlist.title not in existing_playlists:
                playlist_type_instance = existing_playlist_types.get(playlist.playlistType)
                if not playlist_type_instance:
                    raise ValueError(f"Playlist type {playlist.playlistType} not found")
                playlist_instance = Playlist(
                    title=playlist.title,
                    playlist_type_id=playlist_type_instance.id,
                    duration=playlist.duration,
                    thumb=playlist.thumb,
                )
                playlists.append(playlist_instance)
                existing_playlists[playlist.title] = playlist_instance
            else:
                playlist_instance = existing_playlists[playlist.title]
                playlist_instance.duration = playlist.duration
                playlist_instance.thumb = playlist.thumb

            for track in tracks_list:
                # Create Track instances
                track_key = (track.title, track.trackNumber, track.parentTitle, track.grandparentTitle)
                if track_key not in existing_tracks:
                    track_instance = Track(
                        title=track.title,
                        duration=track.duration,
                        album_title=track.parentTitle,
                        artist_name=track.grandparentTitle,
                        track_number=track.trackNumber,
                    )
                    tracks.append(track_instance)
                    existing_tracks[track_key] = track_instance
                else:
                    track_instance = existing_tracks[track_key]
                    track_instance.duration = track.duration
                    track_instance.album_title = track.parentTitle
                    track_instance.artist_name = track.grandparentTitle
                    track_instance.track_number = track.trackNumber

                # Create Album instances
                album_key = (track.parentTitle, track.grandparentTitle)
                if album_key not in existing_albums:
                    album_instance = Album(
                        title=track.parentTitle,
                        thumb=track.parentThumb,
                    )
                    albums.append(album_instance)
                    existing_albums[album_key] = album_instance
                else:
                    album_instance = existing_albums[album_key]
                    album_instance.thumb = track.parentThumb

                # Create Artist instances
                artist_key = track.grandparentTitle
                if artist_key not in existing_artists:
                    genres_string = (
                        ",".join([genre.tag for genre in track.album().artist().genres])
                        if track.album().artist().genres
                        else None
                    )
                    artist_instance = Artist(
                        name=track.grandparentTitle,
                        genres=genres_string,
                    )
                    artists.append(artist_instance)
                    existing_artists[artist_key] = artist_instance
                else:
                    artist_instance = existing_artists[artist_key]

                # Add associations
                playlist_track_associations.append((playlist_instance, track_instance))

                if album_instance and artist_instance:
                    album_artist_associations.append((album_instance, artist_instance))

        # Bulk save all instances
        print("Saving playlists, tracks, albums, and artists to the database.")
        db.session.bulk_save_objects(playlists)
        db.session.bulk_save_objects(tracks)
        db.session.bulk_save_objects(albums)
        db.session.bulk_save_objects(artists)
        db.session.commit()
        print("Committed playlists, tracks, albums, and artists.")

        # Create associations
        print("Creating associations...")
        for playlist_instance, track_instance in playlist_track_associations:
            if track_instance not in playlist_instance.tracks:
                playlist_instance.tracks.append(track_instance)

        for album_instance, artist_instance in album_artist_associations:
            if artist_instance not in album_instance.artists:
                album_instance.artists.append(artist_instance)

        db.session.commit()
        print("All associations have been committed to the database.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
