import os
import asyncio
import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
CHUNK_SECONDS = int(os.getenv("CHUNK_SECONDS", 5))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

async def capture_and_enqueue(channel: str):
    os.makedirs("chunks/raw", exist_ok=True)
    cmd = [
        "ffmpeg",
        "-i", f"https://www.twitch.tv/{channel}",
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-f", "segment",
        "-segment_time", str(CHUNK_SECONDS),
        "-segment_list_type", "csv",
        "-segment_list", "chunks/raw/list.csv",
        "chunks/raw/raw_%03d.wav"
    ]
    proc = await asyncio.create_subprocess_exec(*cmd)
    processed = set()
    while True:
        await asyncio.sleep(1)
        if os.path.exists("chunks/raw/list.csv"):
            with open("chunks/raw/list.csv") as f:
                for line in f.read().splitlines():
                    fname = line.strip()
                    if fname and fname not in processed:
                        processed.add(fname)
                        r.xadd("audio_queue", {"file": fname})