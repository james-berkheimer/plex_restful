import json
import os

from .utils.logging import LOGGER

cred_path = "/home/james/code/plex_restful/tests/.plex_cred/credentials.json"
with open(cred_path, "r") as f:
    data = json.load(f)
    plex_data = data.get("plex", {})
    os.environ["PLEX_BASEURL"] = plex_data.get("baseurl", "")
    os.environ["PLEX_TOKEN"] = plex_data.get("token", "")
    LOGGER.debug(
        "Environment variables set: PLEX_BASEURL = %s , PLEX_TOKEN = %s",
        os.environ["PLEX_BASEURL"],
        os.environ["PLEX_TOKEN"],
    )
