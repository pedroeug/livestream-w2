import { useState, useEffect } from "react";

function App() {
  const [channel, setChannel] = useState("");
  const [started, setStarted] = useState(false);
  const parentDomain = "livestream-w2.onrender.com";

  useEffect(() => {
    if (started && window.Twitch && window.Twitch.Embed) {
      const container = document.getElementById("twitch-embed");
      container.innerHTML = "";

      new window.Twitch.Embed("twitch-embed", {
        width: 854,
        height: 480,
        channel: channel,
        parent: [parentDomain],
        autoplay: true,
        muted: false
      });
    }
  }, [started, channel]);

  const start = async () => {
    await fetch("/api/start-dub", {
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
            onChange={(e) => setChannel(e.target.value)}
          />
          <button
            style={{ marginLeft: 8, padding: "8px 16px" }}
            onClick={start}
          >
            Assistir com Dublagem
          </button>
        </>
      ) : (
        <div style={{ marginTop: 20 }}>
          <div id="twitch-embed" />
          <audio
            controls
            autoPlay
            style={{ display: "block", marginTop: 10 }}
            src={`/api/audio/000`}
          />
          <p>Áudio com ~30s de atraso</p>
        </div>
      )}
    </div>
  );
}

export default App;
