from fastapi import FastAPI, Header, HTTPException
import requests
import os
import time

app = FastAPI()

# Environment variables (set on Render)
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
API_SECRET = os.getenv("MY_API_SECRET")

# Helper function to send message safely
def send_to_discord(message):
    while True:
        try:
            response = requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=10)
            if response.status_code == 429:
                # Discord rate limit hit
                retry_after = response.json().get("retry_after", 1)  # seconds
                print(f"Rate limited! Retrying after {retry_after}s")
                time.sleep(retry_after)
                continue
            response.raise_for_status()  # Raise other HTTP errors
            print("Message sent successfully:", message)
            break
        except requests.exceptions.RequestException as e:
            print("Error sending to Discord:", e)
            # Optional: small delay before retry
            time.sleep(2)

# Health check endpoint
@app.get("/")
def home():
    return {"status": "API running"}

# Main endpoint
@app.post("/send")
async def send_message(data: dict, authorization: str = Header(None)):
    # Check authorization
    if authorization != f"Bearer {API_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    message = data.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="No message provided")

    print("Message to send:", message)
    send_to_discord(message)  # Safe sending with retry
    return {"status": "sent"}
