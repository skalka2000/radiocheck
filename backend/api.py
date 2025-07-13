from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://radiocheck-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "../cache")
RAW_DATA_DIR = os.path.join(BASE_DIR, "../spotify_raw_data")
SPOTIFY_DATA_DIR = os.path.join(BASE_DIR, "../spotify_data")


@app.get("/api/ping")
def ping():
    return {"message": "pong"}

@app.get("/api/top-artists")
def top_artists(start_date: str = None, end_date: str = None):
    print("Fetching top artists with date range:", start_date, end_date)
    try:
        with open(os.path.join(SPOTIFY_DATA_DIR, "filtered_streaming_history.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
        from utilis import filter_by_date_range
        filtered_data = filter_by_date_range(data, start_date, end_date)
        from analyse_data import get_top_artists
        top_artists = get_top_artists(filtered_data, top_n=20)
        return {"artists": top_artists}
    except FileNotFoundError:
        return {"error": "filtered_streaming_history.json not found"}

from fastapi import UploadFile, File
import shutil

@app.post("/api/upload")
async def upload_spotify_file(file: UploadFile = File(...)):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    try:
        file_path = os.path.join(RAW_DATA_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Wait for the main pipeline to process the uploaded file
        import time
        time.sleep(2)  # Adjust this delay as needed
        from main import run_pipeline
        run_pipeline()

        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    
# Delete all imported data
@app.delete("/api/delete-data")
def delete_data():
    try:
        # Remove all files in the raw data directory
        for filename in os.listdir(RAW_DATA_DIR):
            file_path = os.path.join(RAW_DATA_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Remove all files in the Spotify data directory
        for filename in os.listdir(SPOTIFY_DATA_DIR):
            file_path = os.path.join(SPOTIFY_DATA_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return {"status": "success", "message": "All data deleted successfully."}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
