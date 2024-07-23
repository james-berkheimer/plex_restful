from .database import db

# Define the association table between playlists and tracks
playlist_track = db.Table(
    "playlist_track",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("track_id", db.Integer, db.ForeignKey("tracks.id"), primary_key=True),
)

# Define the association table between playlists and albums
playlist_album = db.Table(
    "playlist_album",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("album_id", db.Integer, db.ForeignKey("albums.id"), primary_key=True),
)

# Define the association table between playlists and artists
playlist_artist = db.Table(
    "playlist_artist",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id"), primary_key=True),
)

# Define the association table between tracks and albums
track_album = db.Table(
    "track_album",
    db.Column("track_id", db.Integer, db.ForeignKey("tracks.id"), primary_key=True),
    db.Column("album_id", db.Integer, db.ForeignKey("albums.id"), primary_key=True),
)

# Define the association table between tracks and artists
track_artist = db.Table(
    "track_artist",
    db.Column("track_id", db.Integer, db.ForeignKey("tracks.id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id"), primary_key=True),
)

album_artist = db.Table(
    "album_artist",
    db.Column("album_id", db.Integer, db.ForeignKey("albums.id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id"), primary_key=True),
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

    def __repr__(self):
        playlist_type_name = self.playlist_type.name if self.playlist_type else "None"
        return f"<Playlist(id={self.id}, title={self.title}, playlist_type={playlist_type_name})>"


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
