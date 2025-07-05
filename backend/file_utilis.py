import json
import os

def merge_json_files(folder_path):
    print("MERGE: reading folder_path=", folder_path)
    print("MERGE: contains files:", os.listdir(folder_path))

    # Container for all plays
    all_plays = []

    # Load and merge all JSON files
    for filename in sorted(os.listdir(folder_path)):
        if filename.startswith('Streaming_History') and filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_plays.extend(data)

    print(f"Total plays loaded: {len(all_plays)}")

    # Save merged result
    with open('../spotify_data/merged_streaming_history.json', 'w', encoding='utf-8') as f:
        json.dump(all_plays, f, indent=2)

    print("Merged JSON saved to spotify_data/merged_streaming_history.json")
    return all_plays

def filter_short_plays(play_data, threshold_seconds=30):
    filtered = [
        entry for entry in play_data
        if entry.get("ms_played", 0) >= threshold_seconds * 1000
    ]
    print(f"Filtered out {len(play_data) - len(filtered)} plays under {threshold_seconds} seconds")
    return filtered

def create_song_database(data, output_path='../spotify_data/song_database.json'):
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
                "ms_played": entry.get("ms_played", 0),
                "timestamp": entry.get("ts"),
            }

    # Save the song database to a JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(song_database, f, indent=2)

    print(f"Song database created with {len(song_database)} unique tracks.")
    return song_database

# Create song database from merged data
def prepare_data(folder_path='../spotify_raw_data/'):
    # Merge all JSON files in the folder
    merged_data = merge_json_files(folder_path)

    # Create song database
    create_song_database(merged_data)

    return merged_data