from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/ping")
def ping():
    return {"message": "pong"}

@app.get("/api/top-artists")
def top_artists():
    try:
        with open("cache/top_artists.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"artists": data}
    except FileNotFoundError:
        return {"error": "top_artists.json not found"}
    
from fastapi import UploadFile, File
import shutil

@app.post("/api/upload")
async def upload_spotify_file(file: UploadFile = File(...)):
    file_path = f"spotify_raw_data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Call your processing logic
    from backend.main import run_pipeline
    run_pipeline()

    return {"status": "success"}
