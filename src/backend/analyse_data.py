import os
import json
from collections import Counter
from backend.file_utilis import merge_json_files, filter_short_plays

folder_path = '../spotify_data/'
filename =  "merged_streaming_history.json"

with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
    data = json.load(f)
    # Filter out plays shorter than 30 seconds
    data = filter_short_plays(data, threshold_seconds=30)

def get_top_artists(data, top_n=20):
    """
    Returns the top N most streamed artists by play count.

    Args:
        data (list): List of streaming history entries.
        top_n (int): Number of top artists to return.

    Returns:
        list: List of dicts with keys 'name' and 'play_count'.
    """
    artist_counter = Counter()
    for entry in data:
        artist = entry.get('master_metadata_album_artist_name')
        if artist:
            artist_counter[artist] += 1
    return [
        {"name": artist, "play_count": count}
        for artist, count in artist_counter.most_common(top_n)
    ]

# Example usage:
top_artists = get_top_artists(data, top_n=20)
print("Top 20 most streamed artists (by plays):\n")
for rank, artist_info in enumerate(top_artists, 1):
    print(f"{rank}. {artist_info['name']} – {artist_info['play_count']} plays")