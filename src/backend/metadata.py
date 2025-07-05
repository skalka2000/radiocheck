import os
import json
from collections import Counter
from backend.file_utilis import prepare_data
from backend.spotify_auth import authenticate_spotify
import time


def find_spotify_tracks_by_uri(sp, uri):
    """
    Find a track/tracks on Spotify by their URI.
    """
    # Check if the URI is provided
    if not uri:
        print("No URI provided.")
        return None
    # Check URI type (single string or list of strings)
    if isinstance(uri, str):
        uri = [uri] # Convert to list if it's a single string
    # Check if URI is correctly formatted

    
    try:
        track = sp.track(uri)
        return track
    except Exception as e:
        print(f"Error fetching track for URI {uri}: {e}")
        return None

sp = authenticate_spotify()
# Prepare and load the data
if "filtered_streaming_history.json" not in os.listdir('spotify_data/'):
    print("Filtered data not found, preparing data...")
    data = prepare_data(folder_path='spotify_raw_data/')
else:
    print("Loading existing filtered data...")
    with open('spotify_data/filtered_streaming_history.json', 'r', encoding='utf-8') as f:
        data = json.load(f)    

# Create metadata for all songs
# Count the number of track entries
total = len(data)
print(f"Total tracks in data: {len(data)}")

seen=0

track_metadata = {}
start_time = time.time()

# Iterate through the data and find metadata for each track
print("Starting to fetch track metadata...")
for entry in data:
    uri = entry.get("spotify_track_uri")
    if not uri or uri in track_metadata:
        seen += 1
        if seen % 100 == 0:
            print(f"Processed {seen}/{total} tracks. {seen/total*100:.2f}% complete.")
            # Display time elapsed for processing last 100 tracks
            elapsed = time.time() - start_time
            print(f"Time elapsed for last 100 tracks: {elapsed:.2f} seconds)")
            # Reset start time for next 100 tracks
            start_time = time.time()
        continue

    track = find_song_spotify_by_uri(sp, uri)
    if track:
        time.sleep(0.1)  # 10 requests/sec
        track_metadata[uri] = track
 
    

# Print the number of unique tracks found
print(f"Found metadata for {len(track_metadata)} unique tracks.")

# Save the track metadata to a JSON file
with open('spotify_data/track_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(track_metadata, f, indent=2)


# for entry in data[0:100]:
#     if "spotify_track_uri" in entry:
#         uri = entry["spotify_track_uri"]
#         track = find_song_spotify_by_uri(sp, uri)
#         if track:
#             entry["artists_ids"] = [artist['id'] for artist in track['artists']]
#         else:
#             Exception(f"Track not found for URI: {uri}")

# # Save the updated data with artist IDs
# with open('spotify_data/filtered_streaming_history_with_artist_ids.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, indent=2)

            

