import os
import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import services.stream_capture as sc

app = FastAPI()

# serve SPA React
app.mount(
  "/", 
  StaticFiles(directory="frontend/build", html=True),
  name="frontend"
)

@app.get("/{full_path:path}")
async def spa(full_path: str):
    return FileResponse("frontend/build/index.html")

class StreamRequest(BaseModel):
    channel: str

@app.post("/start-dub")
async def start_dubbing(req: StreamRequest, bg: BackgroundTasks):
    bg.add_task(sc.capture_and_enqueue, req.channel)
    return {"message": f"Dublagem iniciada para canal {req.channel}"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/audio/{block_id}")
def get_audio(block_id: str):
    path = f"chunks/translated_{block_id}.mp3"
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return {"error": "block not found"}