from flask import Blueprint, jsonify, request

from ..database.models import Playlist

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
                "thumbnail": playlist.thumbnail,
            }
        )

    return jsonify(result)


@api_bp.route("/playlists/<int:playlist_id>/items", methods=["GET"])
def get_playlist_items(playlist_id):
    playlist = Playlist.query.get(playlist_id)

    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404

    items_result = []

    for track in playlist.tracks:
        items_result.append(
            {
                "type": "track",
                "track_number": track.track_number,
                "title": track.title,
                "duration": track.duration,
            }
        )

    for episode in playlist.episodes:
        items_result.append(
            {
                "type": "episode",
                "episode_number": episode.episode_number,
                "season_number": episode.season_number,
                "title": episode.title,
                "show_title": episode.show_title,
                "duration": episode.duration,
            }
        )

    for movie in playlist.movies:
        items_result.append(
            {
                "type": "movie",
                "title": movie.title,
                "year": movie.year,
                "duration": movie.duration,
            }
        )

    for photo in playlist.photos:
        items_result.append(
            {
                "type": "photo",
                "title": photo.title,
                "thumbnail": photo.thumbnail,
                "file": photo.file,
            }
        )

    return jsonify(items_result)


@api_bp.route("/playlist_types", methods=["GET"])
def get_playlist_types():
    playlist_types = Playlist.query.with_entities(Playlist.section_type).distinct()
    result = []
    for p_type in playlist_types:
        result.append({"id": p_type.id, "name": p_type.name})
    return jsonify(result)
