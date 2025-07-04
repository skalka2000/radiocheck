import json
import os

def merge_json_files(folder_path):
    # Folder containing JSON files
    # folder_path = 'spotify_raw_data/'

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
    with open('spotify_data/merged_streaming_history.json', 'w', encoding='utf-8') as f:
        json.dump(all_plays, f, indent=2)

    print("Merged JSON saved to spotify_data/merged_streaming_history.json")
    return all_plays
