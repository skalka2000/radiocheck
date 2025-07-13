import json
import os
import hashlib

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "../spotify_raw_data")
SPOTIFY_DATA_DIR = os.path.join(BASE_DIR, "../spotify_data")
CACHE_DIR = os.path.join(BASE_DIR, "../cache")

def hash_dict(d):
    # Create a hash of a dictionary by converting it to a JSON string
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode("utf-8")).hexdigest()

def hash_json_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return hash_dict(data)

def hash_json_folder(folder_path):
    file_hashes = {}

    for root, _, files in os.walk(folder_path):
        for filename in sorted(files):
            if filename.endswith(".json"):
                full_path = os.path.join(root, filename)
                file_hashes[os.path.relpath(full_path, folder_path)] = hash_json_file(full_path)

    return hash_dict(file_hashes)

def get_current_hash(input_hash_path):
    if os.path.exists(input_hash_path):
        with open(input_hash_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None


def merge_json_files(input_folder_path = BASE_DIR, output_folder_path = SPOTIFY_DATA_DIR):
    output_file = os.path.join(output_folder_path, 'merged_streaming_history.json')
    # Get current hash of raw data
    current_raw_hash = get_current_hash(os.path.join(input_folder_path, 'raw_data.hash'))
    new_raw_hash = hash_json_folder(input_folder_path)
    if current_raw_hash == new_raw_hash:
        print("No changes detected in raw data. Skipping merge.")
        # Return Merged data if it exists
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise FileNotFoundError("No merged data found and no changes detected in raw data.")

    # Container for all plays
    all_plays = []

    # Load and merge all JSON files
    for filename in sorted(os.listdir(input_folder_path)):
        if filename.startswith('Streaming_History') and filename.endswith('.json'):
            with open(os.path.join(input_folder_path, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_plays.extend(data)

    print(f"Total plays loaded: {len(all_plays)}")
    # Save merged result
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_plays, f, indent=2)

    print(f"Merged JSON saved to {output_file}")
    return all_plays

def filter_short_plays(play_data, output_folder_path = SPOTIFY_DATA_DIR, threshold_seconds=30):
    output_file = os.path.join(output_folder_path, 'filtered_streaming_history.json')
    filtered = [
        entry for entry in play_data
        if entry.get("ms_played", 0) >= threshold_seconds * 1000
    ]
    print(f"Filtered out {len(play_data) - len(filtered)} plays under {threshold_seconds} seconds")
    # Save filtered data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, indent=2)
    print(f"Filtered data saved to {output_file}")
    return filtered

def create_song_database(data, output_folder_path = SPOTIFY_DATA_DIR):
    output_file = os.path.join(output_folder_path, 'song_database.json')
    # Get the current hash of the song database
    current_db_hash = get_current_hash(os.path.join(output_folder_path, 'song_database.hash'))
    new_db_hash = hash_json_folder(output_folder_path)
    if current_db_hash == new_db_hash:
        print("No changes detected in song database. Skipping creation.")
        # Return existing song database if it exists
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise FileNotFoundError("No song database found and no changes detected in data.")
    # Create database for all unique songs played
    song_database = {}
    for entry in data:
        uri = entry.get("spotify_track_uri")
        # trim uri to remove spotify:track:
        if uri and uri.startswith("spotify:track:"):
            uri = uri[len("spotify:track:"):]
        else:
            Exception("Invalid URI format, expected 'spotify:track:<track_id>'")
        if uri and uri not in song_database:
            # Add all song data to database
            song_database[uri] = {
                "artist": entry.get("master_metadata_album_artist_name"),
                "track_name": entry.get("master_metadata_track_name"),
                "album_name": entry.get("master_metadata_album_album_name"),
            }

    if len(song_database) == 0:
        raise ValueError("No valid songs found in the provided data.")
    # Save the song database to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(song_database, f, indent=2)
    print(f"Song database created with {len(song_database)} unique tracks.")
    return song_database

# Create song database from merged data
def prepare_data(input_folder_path=RAW_DIR, output_folder_path=SPOTIFY_DATA_DIR):

    # Merge all JSON files in the folder
    merged_data = merge_json_files(input_folder_path, output_folder_path)

    if not merged_data:
        raise ValueError("No valid data found in the specified folder.")

    # Create song database
    create_song_database(merged_data, output_folder_path)

    return merged_data