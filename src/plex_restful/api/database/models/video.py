from ...extensions import db
from .associations import playlist_episode, playlist_movie, playlist_season, playlist_show


class Episode(db.Model):
    __tablename__ = "episodes"
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    episode_number = db.Column(db.Integer, nullable=False)
    # season_number = db.Column(db.Integer, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey("seasons.id"), nullable=True)
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"), nullable=True)
    # show_title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    playlists = db.relationship(
        "Playlist", secondary=playlist_episode, back_populates="episodes", lazy="dynamic"
    )

    season = db.relationship("Season", back_populates="episodes")
    show = db.relationship("Show", back_populates="episodes")

    __table_args__ = (db.UniqueConstraint("title", "episode_number", "show_id", name="_episode_uc"),)

    def __repr__(self):
        return f"<Episode(id={self.id}, episode_number={self.episode_number}, title={self.title}, show_id={self.show_id})>"


class Season(db.Model):
    __tablename__ = "seasons"
    id = db.Column(db.Integer, primary_key=True)
    season_number = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"), nullable=True)
    show_title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    show = db.relationship("Show", back_populates="seasons")
    episodes = db.relationship("Episode", back_populates="season")

    playlists = db.relationship(
        "Playlist", secondary=playlist_season, back_populates="seasons", lazy="dynamic"
    )

    __table_args__ = (db.UniqueConstraint("season_number", "show_id", name="_season_uc"),)

    def __repr__(self):
        return f"<Season(id={self.id}, season_number={self.season_number}, show_id={self.show_id})>"


class Show(db.Model):
    __tablename__ = "shows"
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

    episodes = db.relationship("Episode", back_populates="show")
    seasons = db.relationship("Season", back_populates="show", lazy="dynamic")
    playlists = db.relationship(
        "Playlist", secondary=playlist_show, back_populates="shows", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Show(id={self.id}, title={self.title})>"


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=True)
    thumb = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    playlists = db.relationship(
        "Playlist", secondary=playlist_movie, back_populates="movies", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Movie(id={self.id}, title={self.title})>"
