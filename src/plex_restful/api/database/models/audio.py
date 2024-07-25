from ...extensions import db
from .associations import album_artist, playlist_album, playlist_artist, playlist_track


class Track(db.Model):
    __tablename__ = "tracks"
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    track_number = db.Column(db.Integer, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=True)
    album_title = db.Column(db.String(255), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=True)
    artist_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    playlists = db.relationship(
        "Playlist", secondary=playlist_track, back_populates="tracks", lazy="dynamic"
    )
    album = db.relationship("Album", back_populates="tracks")
    artist = db.relationship("Artist", back_populates="tracks")

    __table_args__ = (
        db.UniqueConstraint("title", "track_number", "album_id", "artist_id", name="_track_uc"),
    )

    def __repr__(self):
        return f"<Track(id={self.id}, track_number={self.track_number}, title={self.title}, album_id={self.album_id}, artist_id={self.artist_id})>"


class Album(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    thumb = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    tracks = db.relationship("Track", back_populates="album")
    artists = db.relationship("Artist", secondary=album_artist, back_populates="albums", lazy="dynamic")
    playlists = db.relationship(
        "Playlist", secondary=playlist_album, back_populates="albums", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Album(id={self.id}, title={self.title})>"


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    genres = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    tracks = db.relationship("Track", back_populates="artist")
    albums = db.relationship("Album", secondary=album_artist, back_populates="artists", lazy="dynamic")
    playlists = db.relationship(
        "Playlist", secondary=playlist_artist, back_populates="artists", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Artist(id={self.id}, name={self.name})>"
