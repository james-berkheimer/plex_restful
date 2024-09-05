from flask import Blueprint, jsonify, request

from ..plex.server import get_server
from .database.models import Playlist, Track

plex_server = get_server()

api_bp = Blueprint("api", __name__)


# Example endpoint to fetch playlists
@api_bp.route("/playlists", methods=["GET"])
def get_playlists():
    playlist_type = request.args.get("type")
    if playlist_type:
        playlists = Playlist.query.filter_by(section_type=playlist_type).all()
    else:
        playlists = Playlist.query.all()

    result = []
    for playlist in playlists:
        result.append(
            {
                "id": playlist.id,
                "title": playlist.title,
                "playlist_type": playlist.section_type,
                "duration": playlist.duration,
                "thumb": playlist.thumbnail,
            }
        )

    return jsonify(result)


@api_bp.route("/tracks", methods=["GET"])
def get_all_tracks():
    tracks = Track.query.all()
    result = []
    for track in tracks:
        playlist_titles = [playlist.title for playlist in track.playlists] if track.playlists else None
        result.append(
            {
                "id": track.id,
                "title": track.title,
                "duration": track.duration,
                "track_number": track.track_number,
                "playlist_ids": [playlist.id for playlist in track.playlists],
                "playlist_titles": playlist_titles,
            }
        )
    return jsonify(result)


@api_bp.route("/playlists/<int:playlist_id>/tracks", methods=["GET"])
def get_playlist_tracks(playlist_id):
    # Fetch the playlist by its ID
    playlist = Playlist.query.get(playlist_id)

    # Check if the playlist exists
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    # Prepare the list of tracks
    tracks_result = []
    for track in playlist.tracks:
        tracks_result.append(
            {
                "track_number": track.track_number,
                "title": track.title,
                "duration": track.duration,
            }
        )

    # Return the tracks as a JSON response
    return jsonify(tracks_result)


@api_bp.route("/playlist_types", methods=["GET"])
def get_playlist_types():
    playlist_types = Playlist.query.with_entities(Playlist.section_type).distinct()
    result = []
    for p_type in playlist_types:
        result.append({"id": p_type.id, "name": p_type.name})
    return jsonify(result)
