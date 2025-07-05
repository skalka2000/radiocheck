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


@app.get("/api/ping")
def ping():
    return {"message": "pong"}

@app.get("/api/top-artists")
def top_artists():
    try:
        file_path = os.path.join(CACHE_DIR, "top_artists.json")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"artists": data}
    except FileNotFoundError:
        return {"error": "top_artists.json not found"}

from fastapi import UploadFile, File
import shutil

@app.post("/api/upload")
async def upload_spotify_file(file: UploadFile = File(...)):

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    print()
    try:
        file_path = os.path.join(RAW_DATA_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        from main import run_pipeline
        run_pipeline()

        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
