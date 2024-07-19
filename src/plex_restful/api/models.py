from .database import db

# Define the association table
playlist_track = db.Table(
    "playlist_track",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("track_id", db.Integer, db.ForeignKey("tracks.id"), primary_key=True),
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

    # Define the relationship in Playlist
    tracks = db.relationship(
        "Track", secondary=playlist_track, back_populates="playlists", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Playlist(id={self.id}, title={self.title}, playlist_type={self.playlist_type.name})>"


class Track(db.Model):
    __tablename__ = "tracks"
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    track_number = db.Column(db.Integer, nullable=False)
    album = db.Column(db.String(255), nullable=True)
    artist = db.Column(db.String(255), nullable=True)
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

    __table_args__ = (db.UniqueConstraint("title", "track_number", "album", "artist", name="_track_uc"),)

    def __repr__(self):
        return f"<Track(id={self.id}, track_number={self.track_number}, title={self.title}, album={self.album}, artist={self.artist})>"
