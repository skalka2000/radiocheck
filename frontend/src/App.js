import { useEffect, useState } from "react";

function App() {
  const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const [artists, setArtists] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/top-artists`)
      .then((res) => res.json())
      .then((data) => {
        if (data.artists) setArtists(data.artists);
      })
      .catch((err) => console.error("Error fetching artists:", err));
  }, [API_BASE]);

  const handleUpload = async (e) => {
    const files = e.target.files;
    if (!files.length) return;

    for (const file of files) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const res = await fetch(`${API_BASE}/api/upload`, {
          method: "POST",
          body: formData,
        });

        if (!res.ok) {
          alert(`Upload failed for ${file.name}`);
        }
      } catch (error) {
        console.error(`Upload error for ${file.name}:`, error);
        alert(`Upload error for ${file.name}`);
      }
    }

    alert("All uploads complete. Refreshing stats...");

    const updated = await fetch(`${API_BASE}/api/top-artists`).then((res) =>
      res.json()
    );
    if (updated.artists) setArtists(updated.artists);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Top Artists</h1>

      <input type="file" accept=".json" multiple onChange={handleUpload} />
      <br />
      <br />

      <ol>
        {artists.map((artist, i) => (
          <li key={i} style={{ listStyleType: "decimal" }}>
            {artist.name} — {artist.play_count} plays
          </li>
        ))}
      </ol>
    </div>
  );
}

export default App;
