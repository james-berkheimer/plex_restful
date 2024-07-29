from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker

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
    albums = Table("albums", metadata, autoload_with=engine)

    # Query the database
    result = session.query(albums).all()

    # Print the results
    for row in result:
        print(row.title)


def test2():
    # Reflect the tables
    albums = Table("albums", metadata, autoload_with=engine)
    playlists = Table("playlists", metadata, autoload_with=engine)

    # Query the database
    result = session.query(albums.c.title, playlists.c.title).join(playlists).all()
    for row in result:
        print(row)


def test3():
    pass


def test4():
    pass
