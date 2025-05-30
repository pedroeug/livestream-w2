import os
import redis
import whisper
import requests
import boto3
import time
from dotenv import load_dotenv

load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
VOICE = os.getenv("TTS_VOICE", "Joanna")
DELAY = int(os.getenv("DELAY_SECONDS", 30))

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0)
model = whisper.load_model("base")
polly = boto3.Session(
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET,
    region_name=AWS_REGION
).client("polly")

def translate(text):
    resp = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={"auth_key": DEEPL_API_KEY, "text": text, "target_lang": "EN"}
    )
    return resp.json()["translations"][0]["text"]

def synthesize(text, outpath):
    resp = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=VOICE)
    with open(outpath, "wb") as f:
        f.write(resp["AudioStream"].read())

def worker():
    os.makedirs("chunks/translated", exist_ok=True)
    while True:
        entry = r.xread({"audio_queue": "0-0"}, count=1, block=0)
        if not entry: continue
        _, messages = entry[0]
        for msg_id, data in messages:
            raw_fname = data[b"file"].decode()
            raw_path = f"chunks/raw/{raw_fname}"
            res = model.transcribe(raw_path, language="pt")
            text_pt = res["text"]
            text_en = translate(text_pt)
            idx = raw_fname.split("_")[-1].split(".")[0]
            outp = f"chunks/translated_{idx}.mp3"
            synthesize(text_en, outp)
            time.sleep(DELAY)