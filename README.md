# RadioCheck

**Personal Spotify listening analysis tool.**  
Upload your exported Spotify streaming history and view your top artists.

---

## 🔧 How to Run Locally

### Backend (via Docker)

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/radiocheck.git
   cd radiocheck
2. Build the backend Docker image:
   ```bash
   docker build -t radiocheck-backend .
3. Run the backend container:
   ```bash
   docker run -p 8000:8000 radiocheck-backend
### Frontend
1. Go to the frontend directory
   ```bash
   cd frontend
2. Install dependencies:
   ```bash
   npm install
3. Start the dev server:
   ```bash
   npm start
4. Visit the app at:
   ```bash
   http://localhost:3000