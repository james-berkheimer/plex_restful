from ..plex.data import get_playlist_data
from .database import db
from .models import Album, Artist, Playlist, PlaylistType, Track


def populate_db():
    try:
        db.create_all()

        # Define playlist types
        print("Defining playlist types...")
        playlist_types = ["audio", "photo", "video"]
        created_playlist_types = {}
        for p_type in playlist_types:
            playlist_type_instance = PlaylistType(name=p_type)
            db.session.add(playlist_type_instance)
            created_playlist_types[p_type] = playlist_type_instance
            print(f"Created playlist type: {playlist_type_instance}")

        db.session.commit()
        print("Playlist types committed to database.")

        # Fetch playlist data
        print("Fetching playlist data...")
        playlists_data = get_playlist_data()

        playlists = []
        tracks = []
        albums = []
        artists = []
        playlist_map = {}
        track_map = {}
        album_map = {}
        artist_map = {}

        # Step 1: Create Playlist instances
        print("-------------------> Creating Playlist instances")
        for playlist, tracks_list in playlists_data.items():
            if playlist.title not in playlist_map:
                playlist_type_instance = created_playlist_types.get(playlist.playlistType)
                if not playlist_type_instance:
                    raise ValueError(f"Playlist type {playlist.playlistType} not found")
                playlist_instance = Playlist(
                    title=playlist.title,
                    playlist_type_id=playlist_type_instance.id,
                    duration=playlist.duration,
                    thumb=playlist.thumb,
                )
                playlists.append(playlist_instance)
                playlist_map[playlist.title] = playlist_instance

        print("Saving playlists to the database.")
        db.session.bulk_save_objects(playlists)
        print("Commiting playlists.")
        db.session.commit()

        # Step 2: Create Track instances
        print("-------------------> Creating Track instances")
        for playlist, tracks_list in playlists_data.items():
            for track in tracks_list:
                track_key = (track.title, track.trackNumber, track.parentTitle, track.grandparentTitle)
                if track_key not in track_map:
                    track_instance = Track(
                        title=track.title,
                        duration=track.duration,
                        album_title=track.parentTitle,
                        artist_name=track.grandparentTitle,
                        track_number=track.trackNumber,
                    )
                    tracks.append(track_instance)
                    track_map[track_key] = track_instance

        print("Saving tracks to the database.")
        db.session.bulk_save_objects(tracks)
        print("Commiting tracks.")
        db.session.commit()

        # Step 3: Create Album instances
        print("-------------------> Creating Album instances")
        for playlist, tracks_list in playlists_data.items():
            for track in tracks_list:
                album_key = (track.parentTitle, track.grandparentTitle)
                if album_key not in album_map:
                    album_instance = Album(
                        title=track.parentTitle,
                        thumb=track.parentThumb,
                    )
                    albums.append(album_instance)
                    album_map[album_key] = album_instance

        print("Saving albums to the database.")
        db.session.bulk_save_objects(albums)
        print("Commiting albums.")
        db.session.commit()

        # Step 4: Create Artist instances
        print("-------------------> Creating Artist instances")
        for playlist, tracks_list in playlists_data.items():
            for track in tracks_list:
                artist_key = track.grandparentTitle
                if artist_key not in artist_map:
                    album_object = track.album()
                    artist_object = album_object.artist()
                    if artist_object.genres:
                        genres_string = ",".join([genre.tag for genre in artist_object.genres])
                    else:
                        genres_string = None
                    artist_instance = Artist(
                        name=track.grandparentTitle,
                        genres=genres_string,
                    )
                    artists.append(artist_instance)
                    artist_map[artist_key] = artist_instance

        print("Saving artists to the database.")
        db.session.bulk_save_objects(artists)
        print("Commiting artists.")
        db.session.commit()

        created_playlists = {playlist.title: playlist for playlist in Playlist.query.all()}
        created_tracks = {
            (track.title, track.duration, track.album_title, track.artist_name): track
            for track in Track.query.all()
        }
        created_albums = {album.title: album for album in Album.query.all()}
        created_artists = {artist.name: artist for artist in Artist.query.all()}

        # Step 5: Create associations
        print("-------------------> Creating associations")
        for playlist, tracks_list in playlists_data.items():
            playlist_instance = created_playlists[playlist.title]
            for track in tracks_list:
                track_key = (track.title, track.duration, track.parentTitle, track.grandparentTitle)
                track_instance = created_tracks[track_key]
                playlist_instance.tracks.append(track_instance)

                # Associate Track with Album
                album_instance = created_albums.get(track.parentTitle)
                if album_instance:
                    track_instance.album = album_instance
                    if album_instance not in playlist_instance.albums:
                        playlist_instance.albums.append(album_instance)

                # Associate Track with Artist
                artist_instance = created_artists.get(track.grandparentTitle)
                if artist_instance:
                    track_instance.artist = artist_instance
                    if artist_instance not in playlist_instance.artists:
                        playlist_instance.artists.append(artist_instance)

                # Associate Album with Artist
                if album_instance and artist_instance:
                    if artist_instance not in album_instance.artists:
                        album_instance.artists.append(artist_instance)

            # Ensure playlist is associated with all albums and artists from its tracks
            for track in tracks_list:
                album_instance = created_albums.get(track.parentTitle)
                if album_instance and album_instance not in playlist_instance.albums:
                    playlist_instance.albums.append(album_instance)

                artist_instance = created_artists.get(track.grandparentTitle)
                if artist_instance and artist_instance not in playlist_instance.artists:
                    playlist_instance.artists.append(artist_instance)
        # Commit associations
        print("Commiting associations.")
        db.session.commit()

        print("All playlists, tracks, albums, and artists have been saved to the database.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
