import { useEffect, useState } from "react";

function App() {
  const [artists, setArtists] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/top-artists")
      .then((res) => res.json())
      .then((data) => {
        if (data.artists) setArtists(data.artists);
      })
      .catch((err) => console.error("Error fetching artists:", err));
  }, []);

  return (
    <div>
      <h1>Top Artists</h1>
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
