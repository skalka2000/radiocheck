# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend
COPY cache/ ./cache/
COPY spotify_data/ ./spotify_data/
COPY spotify_raw_data/ ./spotify_raw_data/

# Set working directory inside container
WORKDIR /app/backend

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
