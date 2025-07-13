import { useRef, useEffect, useState } from "react";




function App() {
  const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const [artists, setArtists] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const fileInputRef = useRef(null);


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
    if (fileInputRef.current) {
    fileInputRef.current.value = ""; // reset file input
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <label style={{ marginRight: "0.5rem" }}>
        Start Date: 
        <input
          type="date"
          style={{ marginLeft: "0.5rem" }}
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </label>
      <label style={{ marginLeft: "1rem", marginRight: "0.5rem" }}>
        End Date:
        <input
          type="date"
          style={{ marginLeft: "0.5rem" }}
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </label>
      <button
        style={{ marginLeft: "1rem" }}
        onClick={() => {
          if (startDate && endDate) {
            fetch(`${API_BASE}/api/top-artists?start_date=${startDate}&end_date=${endDate}`)
              .then((res) => res.json())
              .then((data) => {
                if (data.artists) setArtists(data.artists);
              })
              .catch((err) => console.error("Error fetching artists:", err));
          } else {
            alert("Please select both start and end dates.");
          }
        }}
      >
        Filter
      </button>
      <br />
      <br />
      <h1>Top Artists</h1>
      <input type="file" accept=".json" multiple  ref={fileInputRef} onChange={handleUpload} />
      <button
      style={{ marginTop: "1rem", backgroundColor: "#e53935", color: "white", padding: "0.5rem 1rem", border: "none", borderRadius: "4px", cursor: "pointer" }}
      onClick={async () => {
        if (!window.confirm("Are you sure you want to delete all data? This cannot be undone.")) return;

        try {
          const res = await fetch(`${API_BASE}/api/delete-data`, { method: "DELETE" });
          const result = await res.json();

          if (result.status === "success") {
            alert("All data deleted.");
            setArtists([]); // clear local state too
          } else {
            alert("Delete failed: " + result.detail);
          }
        } catch (err) {
          console.error("Delete error:", err);
          alert("Delete request failed.");
        }
      }}
    >
      Delete All Data
    </button>

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
