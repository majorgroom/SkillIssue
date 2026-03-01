from fastapi import FastAPI, Header, HTTPException
import requests
import os

app = FastAPI()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
API_SECRET = os.getenv("MY_API_SECRET")

@app.post("/send")
async def send_message(data: dict, authorization: str = Header(None)):

    if authorization != f"Bearer {API_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    message = data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="No message provided")

    print("Message to send:", message)

    try:
        response = requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=10)
        print("Discord status:", response.status_code)
        print("Discord response:", response.text)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Requests exception:", e)
        raise HTTPException(status_code=500, detail=f"Failed to send to Discord: {e}")

    return {"status": "sent"}
