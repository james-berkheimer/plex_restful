from typing import List, Optional

from sqlalchemy import DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..extensions import db
from .associations import playlist_episode, playlist_movie, playlist_photo, playlist_track


class Playlist(db.Model):
    __tablename__ = "playlists"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    section_type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    thumbnail: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=func.current_timestamp()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    tracks: Mapped[List["Track"]] = relationship(
        "Track", secondary=playlist_track, back_populates="playlists", lazy="dynamic"
    )
    episodes: Mapped[List["Episode"]] = relationship(
        "Episode", secondary=playlist_episode, back_populates="playlists", lazy="dynamic"
    )
    movies: Mapped[List["Movie"]] = relationship(
        "Movie", secondary=playlist_movie, back_populates="playlists", lazy="dynamic"
    )
    photos: Mapped[List["Photo"]] = relationship(
        "Photo", secondary=playlist_photo, back_populates="playlists", lazy="dynamic"
    )


class Track(db.Model):
    __tablename__ = "tracks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    track_number: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    album_title: Mapped[str] = mapped_column(String(255), nullable=False)
    album_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    artist_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=func.current_timestamp()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    playlists: Mapped[List["Playlist"]] = relationship(
        "Playlist", secondary=playlist_track, back_populates="tracks", lazy="dynamic"
    )

    __table_args__ = (
        UniqueConstraint("title", "track_number", "album_title", "artist_name", name="_track_uc"),
    )

    def __repr__(self) -> str:
        return f"<Track(title={self.title}, track_number={self.track_number}, album_title={self.album_title}, artist_name={self.artist_name})>"


class Episode(db.Model):
    __tablename__ = "episodes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    episode_number: Mapped[int] = mapped_column(Integer, nullable=False)
    season_number: Mapped[int] = mapped_column(Integer, nullable=False)
    show_title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    show_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=func.current_timestamp()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    playlists: Mapped[List["Playlist"]] = relationship(
        "Playlist", secondary=playlist_episode, back_populates="episodes", lazy="dynamic"
    )

    __table_args__ = (
        UniqueConstraint("title", "episode_number", "season_number", "show_title", name="_episode_uc"),
    )

    def __repr__(self) -> str:
        return f"<Episode(title={self.title}, episode_number={self.episode_number}, season_number={self.season_number}, show_title={self.show_title})>"


class Movie(db.Model):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    thumbnail: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=func.current_timestamp()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    playlists: Mapped[List["Playlist"]] = relationship(
        "Playlist", secondary=playlist_movie, back_populates="movies", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<Movie(title={self.title}, year={self.year})>"


class Photo(db.Model):
    __tablename__ = "photos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    thumbnail: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    file: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=func.current_timestamp()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    playlists: Mapped[List["Playlist"]] = relationship(
        "Playlist", secondary=playlist_photo, back_populates="photos", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<Photo(title={self.title})>"
