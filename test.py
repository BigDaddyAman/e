import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import httpx
from datetime import datetime
import json

WEBHOOK_CATCHER_URL = os.getenv("WEBHOOK_CATCHER_URL")

app = FastAPI(title="Test Bot Service - Fixed")

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        # Handle empty or non-JSON bodies gracefully
        body = await request.body()
        
        if not body:
            payload = {"message": "Empty webhook received", "timestamp": datetime.now().isoformat()}
        else:
            try:
                # Try to parse as JSON
                payload = await request.json()
            except json.JSONDecodeError:
                # If not JSON, treat as text
                body_text = body.decode('utf-8', errors='replace')
                payload = {
                    "raw_body": body_text,
                    "content_type": request.headers.get("content-type", "unknown"),
                    "timestamp": datetime.now().isoformat()
                }
        
        print("✅ Received webhook:", payload)

        # Forward to Webhook Catcher if set
        if WEBHOOK_CATCHER_URL:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        WEBHOOK_CATCHER_URL, 
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    print(f"📤 Forwarded to catcher (Status: {response.status_code})")
            except Exception as e:
                print("❌ Error forwarding to catcher:", e)

        return {
            "status": "ok", 
            "message": "Webhook received by bot service",
            "timestamp": datetime.now().isoformat(),
            "payload_received": payload
        }
        
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return {
            "status": "error",
            "message": f"Failed to process webhook: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

@app.get("/health")
def health():
    """Health check endpoint - NOW INCLUDED!"""
    return {
        "status": "healthy", 
        "service": "test-bot-fixed",
        "version": "2.1-json-error-fixed",
        "webhook_catcher_configured": bool(WEBHOOK_CATCHER_URL),
        "webhook_catcher_url": WEBHOOK_CATCHER_URL,
        "forwarding_working": bool(WEBHOOK_CATCHER_URL),
        "timestamp": datetime.now().isoformat(),
        "message": "Health endpoint is working! JSON errors fixed! 🎉"
    }
