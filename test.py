import os
from fastapi import FastAPI, Request
import uvicorn
import httpx

WEBHOOK_CATCHER_URL = os.getenv("WEBHOOK_CATCHER_URL")

app = FastAPI()


@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    print("✅ Received webhook:", payload)

    # Forward to Webhook Catcher if set
    if WEBHOOK_CATCHER_URL:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(WEBHOOK_CATCHER_URL, json=payload)
                print("📤 Forwarded to catcher")
        except Exception as e:
            print("❌ Error forwarding to catcher:", e)

    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Bot is running. POST to /webhook"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
