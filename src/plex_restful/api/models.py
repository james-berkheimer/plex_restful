from .database import db


class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    playlist_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    thumb = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Playlist {self.title}>"
