from ...extensions import db

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

# Define the association table between albums and artists
album_artist = db.Table(
    "album_artist",
    db.Column("album_id", db.Integer, db.ForeignKey("albums.id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artists.id"), primary_key=True),
)

# Define the association table between playlists and episodes
playlist_episode = db.Table(
    "playlist_episode",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("episode_id", db.Integer, db.ForeignKey("episodes.id"), primary_key=True),
)

playlist_season = db.Table(
    "playlist_season",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("season_id", db.Integer, db.ForeignKey("seasons.id"), primary_key=True),
)

playlist_show = db.Table(
    "playlist_show",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("show_id", db.Integer, db.ForeignKey("shows.id"), primary_key=True),
)

episode_season = db.Table(
    "episode_season",
    db.Column("episode_id", db.Integer, db.ForeignKey("episodes.id"), primary_key=True),
    db.Column("season_id", db.Integer, db.ForeignKey("seasons.id"), primary_key=True),
)

episode_show = db.Table(
    "episode_show",
    db.Column("episode_id", db.Integer, db.ForeignKey("episodes.id"), primary_key=True),
    db.Column("show_id", db.Integer, db.ForeignKey("shows.id"), primary_key=True),
)

playlist_movie = db.Table(
    "playlist_movie",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id"), primary_key=True),
)


playlist_photo = db.Table(
    "playlist_photo",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlists.id"), primary_key=True),
    db.Column("photo_id", db.Integer, db.ForeignKey("photos.id"), primary_key=True),
)
