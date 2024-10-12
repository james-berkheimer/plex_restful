import traceback

from ...plex.server import get_server
from ..extensions import db
from .models import Episode, Movie, Photo, Playlist, Track


def fetch_existing_data():
    """Fetch existing data from the database and return as dictionaries."""
    data = {
        "playlists": {p.title: p for p in Playlist.query.all()},
        "tracks": {
            (t.title, t.track_number, t.album_title, t.artist_name): t for t in Track.query.all()
        },
        "episodes": {
            (e.title, e.episode_number, e.season_number, e.show_title): e for e in Episode.query.all()
        },
        "movies": {(m.title, m.year, m.duration): m for m in Movie.query.all()},
        "photos": {p.title: p for p in Photo.query.all()},
    }
    print("Existing data fetched.")
    return data


def create_or_update_episode(video, existing_episodes):
    """Create or update an episode entry in the database."""
    show = video.show()
    season = video.season()
    episode_key = (video.title, video.index, season.index, show.title)
    if episode_key not in existing_episodes:
        episode_instance = Episode(
            title=video.title,
            episode_number=video.index,
            duration=video.duration,
            season_number=season.index,
            show_title=show.title,
            show_year=show.year,
        )
        existing_episodes[episode_key] = episode_instance
        return episode_instance
    else:
        episode_instance = existing_episodes[episode_key]
        episode_instance.duration = video.duration
        episode_instance.season_number = season.index
        episode_instance.show_year = show.year
        episode_instance.show_title = show.title
        return episode_instance


def create_or_update_movie(movie, existing_movies):
    """Create or update a movie entry in the database."""
    movie_key = (movie.title, movie.year, movie.duration)
    if movie_key not in existing_movies:
        movie_instance = Movie(
            title=movie.title,
            year=movie.year,
            duration=movie.duration,
            thumbnail=movie.thumb,
        )
        existing_movies[movie_key] = movie_instance
        return movie_instance
    else:
        movie_instance = existing_movies[movie_key]
        movie_instance.duration = movie.duration
        movie_instance.year = movie.year
        movie_instance.title = movie.title
        return movie_instance


def create_or_update_photo(photo, existing_photos):
    """Create or update a photo entry in the database."""
    photo_key = (photo.title, photo.thumb)
    if photo_key not in existing_photos:
        photo_instance = Photo(
            title=photo.title,
            thumbnail=photo.thumb,
            file=photo.media[0].parts[0].file,
        )
        existing_photos[photo_key] = photo_instance
        return photo_instance
    else:
        photo_instance = existing_photos[photo_key]
        photo_instance.thumbnail = photo.thumb
        photo_instance.file = photo.media[0].parts[0].file
        return photo_instance


def create_or_update_playlist(playlist, existing_playlists):
    """Create or update a playlist entry in the database."""
    if playlist.title not in existing_playlists:
        print(f"Creating new playlist: {playlist.title}")
        playlist_instance = Playlist(
            title=playlist.title,
            section_type=playlist.playlistType,
            duration=playlist.duration,
            thumbnail=playlist.thumb,
        )
        existing_playlists[playlist.title] = playlist_instance
        return playlist_instance
    else:
        print(f"Updating existing playlist: {playlist.title}")
        playlist_instance = existing_playlists[playlist.title]
        playlist_instance.section_type = playlist.playlistType
        playlist_instance.duration = playlist.duration
        playlist_instance.thumb = playlist.thumb
        return playlist_instance


def create_or_update_track(track, existing_tracks):
    """Create or update a track entry in the database."""
    album = track.album()
    artist = track.artist()
    track_key = (track.title, track.trackNumber, album.title, artist.title)
    if track_key not in existing_tracks:
        track_instance = Track(
            title=track.title,
            track_number=track.trackNumber,
            duration=track.duration,
            album_title=album.title,
            album_year=album.year,
            artist_name=artist.title,
        )
        existing_tracks[track_key] = track_instance
        return track_instance
    else:
        track_instance = existing_tracks[track_key]
        track_instance.duration = track.duration
        track_instance.album_title = album.title
        track_instance.album_year = album.year
        track_instance.artist_name = artist.title
        return track_instance


def save_playlists(playlists, existing_playlists):
    """Save playlists to the database."""
    playlist_instances = []

    for playlist in playlists:
        print(f"Processing playlist: {playlist.title}\n")
        playlist_instance = create_or_update_playlist(playlist, existing_playlists)
        playlist_instances.append(playlist_instance)

    # Bulk save all instances
    print("Saving playlists.")
    db.session.bulk_save_objects(playlist_instances)
    print("Committed playlists.")


def populate_database():
    """Populate the database with data from the Plex server."""
    track_instances = []
    episode_instances = []
    movie_instances = []
    photo_instances = []
    processed_items = set()

    try:
        print("Connecting to Plex server...")
        plex_server = get_server()
        playlists = plex_server.playlists()

        print("Fetching existing data...")
        existing_data = fetch_existing_data()

        # Save playlists
        save_playlists(playlists, existing_data["playlists"])

        print("Processing playlist items...")
        # Save playlist data
        for playlist in playlists:
            playlist_instance = existing_data["playlists"][playlist.title]
            for item in playlist.items():
                if item.ratingKey not in processed_items:
                    processed_items.add(item.ratingKey)
                    if playlist.playlistType == "audio":
                        # print(f"Processing tracks for playlist: {playlist.title}")
                        # print(f"Playlist has {len(playlist.items())} tracks.")
                        track_instance = create_or_update_track(item, existing_data["tracks"])
                        track_instances.append(track_instance)
                    elif playlist.playlistType == "video":
                        if item.type == "episode":
                            episode_instance = create_or_update_episode(item, existing_data["episodes"])
                            episode_instances.append(episode_instance)
                        if item.type == "movie":
                            movie_instance = create_or_update_movie(item, existing_data["movies"])
                            movie_instances.append(movie_instance)
                    elif playlist.playlistType == "photo":
                        photo_instance = create_or_update_photo(item, existing_data["photos"])
                        photo_instances.append(photo_instance)
                else:
                    if playlist.playlistType == "audio":
                        track_instance = existing_data["tracks"][
                            (item.title, item.trackNumber, item.album().title, item.artist().title)
                        ]
                    elif playlist.playlistType == "video":
                        if item.type == "episode":
                            episode_instance = existing_data["episodes"][
                                (item.title, item.index, item.season().index, item.show().title)
                            ]
                        if item.type == "movie":
                            movie_instance = existing_data["movies"][
                                (item.title, item.year, item.duration)
                            ]
                    elif playlist.playlistType == "photo":
                        photo_instance = existing_data["photos"][item.title]

                # Add item to the playlist
                if playlist.playlistType == "audio":
                    playlist_instance.tracks.append(track_instance)
                elif playlist.playlistType == "video":
                    if item.type == "episode":
                        playlist_instance.episodes.append(episode_instance)
                    if item.type == "movie":
                        playlist_instance.movies.append(movie_instance)
                elif playlist.playlistType == "photo":
                    playlist_instance.photos.append(photo_instance)

            # Add playlist instance to the session
            db.session.add(playlist_instance)

        # Bulk save all instances
        print("Saving tracks.")
        db.session.bulk_save_objects(track_instances)
        print("Saving episodes.")
        db.session.bulk_save_objects(episode_instances)
        print("Saving movies.")
        db.session.bulk_save_objects(movie_instances)
        print("Saving photos.")
        db.session.bulk_save_objects(photo_instances)

        print("Committing session.")
        db.session.commit()
        print("Database populated successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
        db.session.rollback()
