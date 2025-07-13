import os
import json
from collections import Counter
from file_utilis import prepare_data
from spotify_auth import authenticate_spotify
import time



def fetch_spotify_track_metadata(data, sp, output_path='../spotify_data/track_metadata.json', batch_size=50):
    """
    Fetches track metadata from Spotify for all tracks in data and saves it to a JSON file.

    Args:
        data (dict): Dictionary where keys are 'spotify_track_uri'.
        sp: Authenticated Spotify client.
        output_path (str): Path to save the metadata JSON.
        batch_size (int): Number of URIs to fetch per batch.
    """
    uris_to_fetch = list(data.keys())
    total = len(uris_to_fetch)
    print(f"Total unique track URIs in data: {total}")

    track_metadata = {}
    print("Starting to fetch track metadata...")

    for i in range(0, total, batch_size):
        batch = uris_to_fetch[i:i + batch_size]
        try:
            results = sp.tracks(batch)
            for track in results['tracks']:
                if track:  # Track might be None if URI is invalid
                    track_id = track['id']
                    if track_id in data:
                        track_metadata[track_id] = track

        except Exception as e:
            print(f"Error fetching batch {i}-{i+batch_size}: {e}")

        time.sleep(0.1)  # Throttle to ~10 requests/sec if needed   

    print(f"Found metadata for {len(track_metadata)} unique tracks.")

    # Print first 10 keys
    print("Sample track metadata keys:", list(track_metadata.keys())[:10])

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(track_metadata, f, indent=2)



            

