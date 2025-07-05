from backend.file_utilis import merge_json_files
from backend.file_utilis import prepare_data
from backend.file_utilis import filter_short_plays
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

    # # Check if the merged data file exists, if not, prepare the data
    # if "merged_streaming_history.json" not in os.listdir(SPOTIFY_DATA_DIR):
        # print("Merged data not found, preparing data...")
    merged_data = prepare_data(folder_path=RAW_DIR)
    print(f"Merged data created with {len(merged_data)} entries from {RAW_DIR}.")
    # else:
    #     print("Loading existing merged data...")
    #     with open(merged_file_path, 'r', encoding='utf-8') as f:
    #         merged_data = json.load(f)
    
    # Filter out plays shorter than 30 seconds
    filtered_data = filter_short_plays(merged_data, threshold_seconds=30)
    print(f"Filtered data contains {len(filtered_data)} entries after removing short plays.")
    # Save the filtered data
    with open(filtered_file_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2)
        print(f"Filtered data saved to {filtered_file_path}")
    
    # Retrieve Song Database
    with open(song_db_path, 'r', encoding='utf-8') as f:
        song_database = json.load(f)
    print(f"Loaded song database with {len(song_database)} unique tracks.")

    # Generate Top Artists
    from backend.analyse_data import get_top_artists
    top_artists = get_top_artists(filtered_data, top_n=20)
    
    # Save Top Artists to cache
    with open(top_artists_cache_path, 'w', encoding='utf-8') as f:
        json.dump(top_artists, f, indent=2)
        print(f"Top artists saved to {top_artists_cache_path}")

def main():
    print("Starting the Spotify data processing pipeline...")
    run_pipeline()
    print("Pipeline completed successfully.")   