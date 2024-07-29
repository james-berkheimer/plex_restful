from ...extensions import db
from .associations import (
    playlist_album,
    playlist_artist,
    playlist_episode,
    playlist_season,
    playlist_show,
    playlist_track,
)


class PlaylistType(db.Model):
    __tablename__ = "playlist_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<PlaylistType(id={self.id}, name={self.name})>"


class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=True)
    playlist_type_id = db.Column(db.Integer, db.ForeignKey("playlist_types.id"), nullable=False)
    playlist_type = db.relationship("PlaylistType", backref=db.backref("playlists", lazy=True))
    thumb = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(255), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    tracks = db.relationship(
        "Track", secondary=playlist_track, back_populates="playlists", lazy="dynamic"
    )
    albums = db.relationship(
        "Album", secondary=playlist_album, back_populates="playlists", lazy="dynamic"
    )
    artists = db.relationship(
        "Artist", secondary=playlist_artist, back_populates="playlists", lazy="dynamic"
    )

    episodes = db.relationship(
        "Episode", secondary=playlist_episode, back_populates="playlists", lazy="dynamic"
    )

    seasons = db.relationship(
        "Season", secondary=playlist_season, back_populates="playlists", lazy="dynamic"
    )

    shows = db.relationship("Show", secondary=playlist_show, back_populates="playlists", lazy="dynamic")

    def __repr__(self):
        playlist_type_name = self.playlist_type.name if self.playlist_type else "None"
        return f"<Playlist(id={self.id}, title={self.title}, playlist_type={playlist_type_name})>"
