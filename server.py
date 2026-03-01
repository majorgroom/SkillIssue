from fastapi import FastAPI, Header, HTTPException
import requests
import os

app = FastAPI()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
API_SECRET = os.getenv("MY_API_SECRET")

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/send")
async def send_message(data: dict, authorization: str = Header(None)):

    if authorization != f"Bearer {API_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    message = data.get("message")

    if not message:
        raise HTTPException(status_code=400, detail="No message provided")

    requests.post(DISCORD_WEBHOOK, json={"content": message})

    return {"status": "sent"}