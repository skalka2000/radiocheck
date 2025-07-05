import json
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from time import sleep



def authenticate_spotify():
    """
    Authenticate with Spotify using client credentials.
    Returns a Spotify client instance.
    """
    # Ensure environment variables are loaded
    if not os.getenv("SPOTIFY_CLIENT_ID") or not os.getenv("SPOTIFY_CLIENT_SECRET"):
        raise ValueError("Spotify client ID and secret must be set in environment variables.")

    # Load environment variables
    load_dotenv()

    # Get credentials from environment variables
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    # Authenticate with Spotify
    sp = Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

    return sp

# # Load environment variables
# load_dotenv()
# client_id = os.getenv("SPOTIFY_CLIENT_ID")
# client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# # Authenticate
# sp = Spotify(auth_manager=SpotifyClientCredentials(
#     client_id=client_id,
#     client_secret=client_secret
# ))

