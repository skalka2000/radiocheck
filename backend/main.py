from file_utilis import merge_json_files
from file_utilis import prepare_data
from file_utilis import filter_short_plays
from metadata import fetch_spotify_track_metadata
from spotify_auth import authenticate_spotify
from file_utilis import get_current_hash, hash_json_file
import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "../spotify_raw_data")
SPOTIFY_DATA_DIR = os.path.join(BASE_DIR, "../spotify_data")
CACHE_DIR = os.path.join(BASE_DIR, "../cache")



def run_pipeline():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(SPOTIFY_DATA_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    merged_file_path = os.path.join(SPOTIFY_DATA_DIR, "merged_streaming_history.json")
    filtered_file_path = os.path.join(SPOTIFY_DATA_DIR, "filtered_streaming_history.json")
    song_db_path = os.path.join(SPOTIFY_DATA_DIR, "song_database.json")
    top_artists_cache_path = os.path.join(CACHE_DIR, "top_artists.json")
    song_db_hash_path = os.path.join(SPOTIFY_DATA_DIR, "song_database.hash")
    merged_hash_path = os.path.join(SPOTIFY_DATA_DIR, "merged_streaming_history.hash")

    # Merge data from raw JSON files
    merged_data = prepare_data(input_folder_path=RAW_DIR, output_folder_path=SPOTIFY_DATA_DIR)
    print(f"Merged data created with {len(merged_data)} entries from {RAW_DIR}.")
    
    # Filter out plays shorter than 30 seconds
    filtered_data = filter_short_plays(merged_data, threshold_seconds=30)
    print(f"Filtered data contains {len(filtered_data)} entries after removing short plays.")
    
    # Retrieve Song Database
    with open(song_db_path, 'r', encoding='utf-8') as f:
        song_database = json.load(f)
    print(f"Loaded song database with {len(song_database)} tracks.")
    # Generate hash for the song database
    current_db_hash = get_current_hash(song_db_hash_path)
    new_db_hash = hash_json_file(song_db_path)
    if current_db_hash == new_db_hash:
        print("No changes detected in song database.")
        return
    else:
        print("Changes detected in song database. Proceeding with metadata fetching.")
        sp = authenticate_spotify()
        fetch_spotify_track_metadata(song_database, sp, output_path=os.path.join(SPOTIFY_DATA_DIR, "track_metadata.json"))
    
    
    # # Save Top Artists to cache
    # with open(top_artists_cache_path, 'w', encoding='utf-8') as f:
    #     json.dump(top_artists, f, indent=2)
    #     print(f"Top artists saved to {top_artists_cache_path}")

def main():
    print("Starting the Spotify data processing pipeline...")
    run_pipeline()
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()