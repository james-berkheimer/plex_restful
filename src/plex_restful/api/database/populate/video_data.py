from ....plex.data import get_playlist_data
from ...extensions import db
from ..models import Episode, Movie, Playlist, PlaylistType, Season, Show


def populate_video_data():
    try:
        # Fetch playlist types
        existing_playlist_types = {ptype.name: ptype for ptype in PlaylistType.query.all()}

        # Fetch playlist data
        print("Fetching playlist data...")
        playlists_data = get_playlist_data()

        # Pre-fetch existing data
        existing_playlists = {p.title: p for p in Playlist.query.all()}
        existing_episodes = {
            (e.title, e.episode_number, e.season_title, e.show_name): e for e in Episode.query.all()
        }
        existing_seasons = {s.title: s for s in Season.query.all()}
        existing_shows = {sh.name: sh for sh in Show.query.all()}

        playlists = []
        episodes = []
        seasons = []
        shows = []
        playlist_episode_associations = []
        season_show_associations = []

        print("Creating instances for playlists, episodes, seasons, and shows...")
        for playlist, episodes_list in playlists_data.items():
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

            for episode in episodes_list:
                # Create Episode instances
                episode_key = (
                    episode.title,
                    episode.episodeNumber,
                    episode.parentTitle,
                    episode.grandparentTitle,
                )
                if episode_key not in existing_episodes:
                    episode_instance = Episode(
                        title=episode.title,
                        duration=episode.duration,
                        season_title=episode.parentTitle,
                        show_name=episode.grandparentTitle,
                        episode_number=episode.index,
                    )
                    episodes.append(episode_instance)
                    existing_episodes[episode_key] = episode_instance
                else:
                    episode_instance = existing_episodes[episode_key]
                    episode_instance.duration = episode.duration
                    episode_instance.season_title = episode.parentTitle
                    episode_instance.show_name = episode.grandparentTitle
                    episode_instance.episode_number = episode.index

                # Create Season instances
                season_key = (episode.parentTitle, episode.grandparentTitle)
                if season_key not in existing_seasons:
                    season_instance = Season(
                        title=episode.parentTitle,
                        thumb=episode.parentThumb,
                    )
                    seasons.append(season_instance)
                    existing_seasons[season_key] = season_instance
                else:
                    season_instance = existing_seasons[season_key]
                    season_instance.thumb = episode.parentThumb

                # Create Show instances
                show_key = episode.grandparentTitle
                if show_key not in existing_shows:
                    genres_string = (
                        ",".join([genre.tag for genre in episode.season().show().genres])
                        if episode.season().show().genres
                        else None
                    )
                    show_instance = Show(
                        name=episode.grandparentTitle,
                        genres=genres_string,
                    )
                    shows.append(show_instance)
                    existing_shows[show_key] = show_instance
                else:
                    show_instance = existing_shows[show_key]

                # Add associations
                playlist_episode_associations.append((playlist_instance, episode_instance))

                if season_instance and show_instance:
                    season_show_associations.append((season_instance, show_instance))

        # Bulk save all instances
        print("Saving playlists, episodes, seasons, and shows to the database.")
        db.session.bulk_save_objects(playlists)
        db.session.bulk_save_objects(episodes)
        db.session.bulk_save_objects(seasons)
        db.session.bulk_save_objects(shows)
        db.session.commit()
        print("Committed playlists, episodes, seasons, and shows.")

        # Create associations
        print("Creating associations...")
        for playlist_instance, episode_instance in playlist_episode_associations:
            if episode_instance not in playlist_instance.episodes:
                playlist_instance.episodes.append(episode_instance)

        for season_instance, show_instance in season_show_associations:
            if show_instance not in season_instance.shows:
                season_instance.shows.append(show_instance)

        db.session.commit()
        print("All associations have been committed to the database.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
