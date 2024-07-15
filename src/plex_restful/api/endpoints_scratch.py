from flask import Blueprint, jsonify, request

from ..plex.server import get_server
from .models import Playlist, db

plex_server = get_server()


api_bp = Blueprint("api", __name__)


# Example endpoint to fetch playlists
@api_bp.route("/playlists", methods=["GET"])
def get_playlists():
    playlist_type = request.args.get("type")
    if playlist_type:
        playlists = Playlist.query.filter_by(playlist_type=playlist_type).all()
    else:
        playlists = Playlist.query.all()

    result = []
    for playlist in playlists:
        result.append(
            {
                "title": playlist.title,
                "playlist_type": playlist.playlist_type,
                "duration": playlist.duration,
                "thumb": playlist.thumb,
            }
        )

    return jsonify(result)


# Example endpoint to populate playlists from Plex
@api_bp.route("/populate", methods=["POST"])
def populate_playlists():
    for plex_playlist in plex_server.playlists():
        playlist = Playlist(
            title=plex_playlist.title,
            playlist_type=plex_playlist.playlistType,
            duration=plex_playlist.duration,
            thumb=plex_playlist.thumb,
        )
        db.session.add(playlist)
    db.session.commit()

    return jsonify({"message": "Playlists populated successfully"})
