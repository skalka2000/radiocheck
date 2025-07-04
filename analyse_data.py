import os
import json
folder_path = 'spotify_data/'
filename =  "merged_streaming_history.json"

with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data[0])