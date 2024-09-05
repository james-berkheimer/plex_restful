from sqlalchemy import Column, ForeignKey, Integer, Table

from ..extensions import db

playlist_track = Table(
    "playlist_track",
    db.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
)

playlist_episode = Table(
    "playlist_episode",
    db.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("episode_id", Integer, ForeignKey("episodes.id"), primary_key=True),
)

playlist_movie = Table(
    "playlist_movie",
    db.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
)

playlist_photo = Table(
    "playlist_photo",
    db.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("photo_id", Integer, ForeignKey("photos.id"), primary_key=True),
)
