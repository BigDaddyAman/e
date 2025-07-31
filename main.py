import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import httpx
from datetime import datetime

WEBHOOK_CATCHER_URL = os.getenv("WEBHOOK_CATCHER_URL")

app = FastAPI(title="Test Bot Service")

@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    print("✅ Received webhook:", payload)

    # Forward to Webhook Catcher if set
    if WEBHOOK_CATCHER_URL:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(WEBHOOK_CATCHER_URL, json=payload)
                print(f"📤 Forwarded to catcher (Status: {response.status_code})")
        except Exception as e:
            print("❌ Error forwarding to catcher:", e)

    return {
        "status": "ok", 
        "message": "Webhook received by bot service",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
def root():
    # Add a simple HTML interface
    webhook_status = "✅ Connected" if WEBHOOK_CATCHER_URL else "❌ Not configured"
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Bot Service</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 2rem; max-width: 600px; margin: 0 auto; }}
            .status {{ padding: 1rem; margin: 1rem 0; border-radius: 8px; }}
            .connected {{ background: #d4edda; color: #155724; }}
            .disconnected {{ background: #f8d7da; color: #721c24; }}
            pre {{ background: #f8f9fa; padding: 1rem; border-radius: 4px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>🤖 Test Bot Service</h1>
        <p>Bot is running and ready to receive webhooks!</p>
        
        <div class="status {'connected' if WEBHOOK_CATCHER_URL else 'disconnected'}">
            <strong>Webhook Catcher:</strong> {webhook_status}<br>
            <strong>URL:</strong> {WEBHOOK_CATCHER_URL or 'Not set'}
        </div>
        
        <h3>Test with cURL:</h3>
        <pre>curl -X POST https://{os.getenv('RAILWAY_PUBLIC_DOMAIN', 'your-bot-domain.railway.app')}/webhook \\
  -H "Content-Type: application/json" \\
  -d '{{"event": "test", "message": "Hello Bot!"}}'</pre>
        
        <p>Send POST requests to <code>/webhook</code> to test the bot and forwarding.</p>
    </body>
    </html>
    """)

@app.get("/health")
def health():
    return {
        "status": "healthy", 
        "service": "test-bot",
        "webhook_catcher_configured": bool(WEBHOOK_CATCHER_URL),
        "webhook_catcher_url": WEBHOOK_CATCHER_URL,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run("test:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

web: uvicorn test:app --host=0.0.0.0 --port=${PORT:-8000}
