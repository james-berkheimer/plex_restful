from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker

from .database.models import Playlist

db_path = "sqlite:///src/instance/plex_restful.db"
# Create an engine and connect to the database
engine = create_engine(db_path)
metadata = MetaData()
metadata.reflect(bind=engine)
# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def test1():
    # Reflect the tables
    playlists = Table("playlists", metadata, autoload_with=engine)

    # Query the database
    result = session.query(playlists).all()

    # Print the results
    for playlist in result:
        total_relationships = playlist.count_relationships()
        print(
            f"{playlist.title}: Duration: {playlist.duration} seconds, Total Relationships: {total_relationships}"
        )


def test2():
    # Reflect the tables
    albums = Table("albums", metadata, autoload_with=engine)
    playlists = Table("playlists", metadata, autoload_with=engine)

    # Query the database
    result = session.query(albums.c.title, playlists.c.title).join(playlists).all()
    for row in result:
        print(row)


def test3():
    playlists = session.query(Playlist).all()

    for playlist in playlists:
        total_relationships = playlist.count_relationships()
        print(total_relationships)
        print(f"Tracks: {playlist.tracks.count()}")
        print(f"{playlist.title}: Duration: {playlist.duration} seconds")


def test4():
    playlist_lst = session.query(Playlist).filter(Playlist.title == "test video").all()
    playlist = playlist_lst[0]
    print(f"{playlist.title}: {playlist.episodes.count()} episodes")
    items = playlist.episodes.all()
    for item in items:
        print(f"  {item.title}")
