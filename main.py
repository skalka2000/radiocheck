from file_utilis import merge_json_files

if __name__ == "__main__":
    folder_path = 'spotify_raw_data/'
    data = merge_json_files(folder_path)
    print(data[0])