import { useState } from "react";

function App() {
  const [channel, setChannel] = useState("");
  const [started, setStarted] = useState(false);

  const start = async () => {
    await fetch("/start-dub", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ channel })
    });
    setStarted(true);
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h1>Livestream W2 – Twitch Dub</h1>
      {!started ? (
        <>
          <input
            style={{ padding: 8, width: 300 }}
            placeholder="Canal da Twitch"
            value={channel}
            onChange={e => setChannel(e.target.value)}
          />
          <button style={{ marginLeft: 8, padding: "8px 16px" }} onClick={start}>
            Assistir com Dublagem
          </button>
        </>
      ) : (
        <div style={{ marginTop: 20 }}>
          <iframe
            src={`https://player.twitch.tv/?channel=${channel}&parent=livestream-w2-demo.onrender.com&autoplay=true&muted=false`}
            height="360"
            width="640"
            allowFullScreen
          />
          <audio
            controls
            autoPlay
            style={{ display: "block", marginTop: 10 }}
            src={`/audio/000`} 
          />
          <p>Áudio com ~30s de atraso</p>
        </div>
      )}
    </div>
  );
}

export default App;