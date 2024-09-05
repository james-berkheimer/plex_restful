from ...plex.server import get_server
from ..extensions import db
from .models import Episode, Movie, Photo, Playlist, Track


def fetch_existing_data():
    print("Fetching existing data from the database...")
    data = {
        "playlists": {p.title: p for p in Playlist.query.all()},
        "tracks": {t.title: t for t in Track.query.all()},
        "episodes": {e.title: e for e in Episode.query.all()},
        "movies": {m.title: m for m in Movie.query.all()},
        "photos": {p.title: p for p in Photo.query.all()},
    }
    print("Existing data fetched.")
    return data


def create_or_update_playlist(playlist, existing_playlists):
    print(f"Processing playlist: {playlist.title}")
    if playlist.title not in existing_playlists:
        print(f"Creating new playlist: {playlist.title}")
        playlist_instance = Playlist(
            title=playlist.title,
            section_type=playlist.playlistType,
            duration=playlist.duration,
            thumbnail=playlist.thumb,
        )
        existing_playlists[playlist.title] = playlist_instance
        return playlist_instance, True
    else:
        print(f"Updating existing playlist: {playlist.title}")
        playlist_instance = existing_playlists[playlist.title]
        playlist_instance.section_type = playlist.playlistType
        playlist_instance.duration = playlist.duration
        playlist_instance.thumb = playlist.thumb
        return playlist_instance, False


def create_or_update_track(track, existing_tracks):
    album = track.album()
    artist = track.artist()
    track_key = (track.title, track.trackNumber, album.title, artist.title)
    print(f"Processing track: {track.title}")
    if track_key not in existing_tracks:
        print(f"Creating new track: {track.title}")
        track_instance = Track(
            title=track.title,
            track_number=track.trackNumber,
            duration=track.duration,
            album_title=album.title,
            album_year=album.year,
            artist_name=artist.title,
        )
        existing_tracks[track_key] = track_instance
        return track_instance, True
    else:
        print(f"Updating existing track: {track.title}")
        track_instance = existing_tracks[track_key]
        track_instance.duration = track.duration
        track_instance.album_title = album.title
        track_instance.album_year = album.year
        track_instance.artist_name = artist.title
        return track_instance, False


def create_or_update_episode(video, existing_episodes):
    show = video.show()
    season = video.season()
    episode_key = (video.title, video.index, season.index, show.title)
    print(f"Processing episode: {video.title}")
    if episode_key not in existing_episodes:
        print(f"Creating new episode: {video.title}")
        episode_instance = Episode(
            title=video.title,
            episode_number=video.index,
            duration=video.duration,
            season_number=season.index,
            show_title=show.title,
            show_year=show.year,
        )
        existing_episodes[episode_key] = episode_instance
        return episode_instance, True
    else:
        print(f"Updating existing episode: {video.title}")
        episode_instance = existing_episodes[episode_key]
        episode_instance.duration = video.duration
        episode_instance.season_number = season.index
        episode_instance.show_year = show.year
        episode_instance.show_title = show.title
        return episode_instance, False


def create_or_update_movie(video, existing_movies):
    movie_key = (video.title, video.year)
    print(f"Processing movie: {video.title}")
    if movie_key not in existing_movies:
        print(f"Creating new movie: {video.title}")
        movie_instance = Movie(
            title=video.title,
            duration=video.duration,
            year=video.year,
            thumbnail=video.thumb,
        )
        existing_movies[movie_key] = movie_instance
        return movie_instance, True
    else:
        print(f"Updating existing movie: {video.title}")
        movie_instance = existing_movies[movie_key]
        movie_instance.duration = video.duration
        movie_instance.thumbnail = video.thumb
        movie_instance.year = video.year
        movie_instance.title = video.title
        return movie_instance, False


def create_or_update_video(video, existing_episodes, existing_movies):
    if video.type == "episode":
        return create_or_update_episode(video, existing_episodes)
    elif video.type == "movie":
        return create_or_update_movie(video, existing_movies)
    else:
        return None, False


def create_or_update_photo(photo, existing_photos):
    photo_key = photo.title
    print(f"Processing photo: {photo.title}")
    if photo_key not in existing_photos:
        print(f"Creating new photo: {photo.title}")
        photo_instance = Photo(
            title=photo.title,
            thumbnail=photo.thumb,
            file=photo.media[0].parts[0].file,
        )
        existing_photos[photo_key] = photo_instance
        return photo_instance, True
    else:
        print(f"Updating existing photo: {photo.title}")
        photo_instance = existing_photos[photo_key]
        photo_instance.thumbnail = photo.thumb
        photo_instance.file = photo.media[0].parts[0].file
        return photo_instance, False


def handle_associations(
    playlist_instance, items, association_list, existing_items, create_or_update_func
):
    for item in items:
        item_instance, is_new = create_or_update_func(item, existing_items)
        if item_instance not in getattr(playlist_instance, association_list):
            print(f"Associating {item_instance} with playlist {playlist_instance.title}")
            getattr(playlist_instance, association_list).append(item_instance)


def populate_database():
    try:
        print("Connecting to Plex server...")
        plex_server = get_server()
        print("Fetching existing data...")
        existing_data = fetch_existing_data()

        playlists = []
        tracks = []
        episodes = []
        movies = []
        photos = []

        for playlist in plex_server.playlists():
            print(f"Processing playlist: {playlist.title}")
            playlist_instance, is_new = create_or_update_playlist(playlist, existing_data["playlists"])
            if is_new:
                playlists.append(playlist_instance)

            if playlist.playlistType == "audio":
                handle_associations(
                    playlist_instance,
                    playlist.items(),
                    "tracks",
                    existing_data["tracks"],
                    create_or_update_track,
                )

            if playlist.playlistType == "video":
                handle_associations(
                    playlist_instance,
                    playlist.items(),
                    "episodes",
                    existing_data["episodes"],
                    create_or_update_episode,
                )
                handle_associations(
                    playlist_instance,
                    playlist.items(),
                    "movies",
                    existing_data["movies"],
                    create_or_update_movie,
                )

            if playlist.playlistType == "photo":
                handle_associations(
                    playlist_instance,
                    playlist.items(),
                    "photos",
                    existing_data["photos"],
                    create_or_update_photo,
                )

        # Bulk save all instances
        print("Saving playlists, tracks, episodes, movies, and photos to the database.")
        db.session.bulk_save_objects(playlists)
        db.session.bulk_save_objects(tracks)
        db.session.bulk_save_objects(episodes)
        db.session.bulk_save_objects(movies)
        db.session.bulk_save_objects(photos)
        print("Committed playlists, tracks, episodes, movies, and photos.")

        db.session.commit()
        print("All associations have been committed to the database.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
