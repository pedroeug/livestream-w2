import os
import asyncio
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import services.stream_capture as sc

app = FastAPI()

# --- ROTAS DE API (prefixo /api) ---

class StreamRequest(BaseModel):
    channel: str

@app.post("/api/start-dub")
async def start_dubbing(req: StreamRequest, bg: BackgroundTasks):
    bg.add_task(sc.capture_and_enqueue, req.channel)
    return {"message": f"Dublagem iniciada para canal {req.channel}"}

@app.get("/api/audio/{block_id}")
def get_audio(block_id: str):
    path = f"chunks/translated_{block_id}.mp3"
    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return {"error": "block not found"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

# --- SERVE O FRONTEND (SPA) ---

# 1) Monta todos os arquivos estáticos do React
app.mount(
    "/",
    StaticFiles(directory="frontend/build", html=True),
    name="frontend"
)

# 2) Fallback: qualquer GET que não bater em arquivo estático
@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    return FileResponse("frontend/build/index.html")
