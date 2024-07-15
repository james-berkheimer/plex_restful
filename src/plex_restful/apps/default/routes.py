from flask import Blueprint, render_template

default_bp = Blueprint("default", __name__)


@default_bp.route("/")
def default():
    return render_template("index.html")


# Example route
# @app.route("/")
# def index():
#     new_playlist = Playlist(name="New Playlist")
#     db.session.add(new_playlist)
#     db.session.commit()
#     return "Playlist added!"
