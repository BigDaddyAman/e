import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import httpx
from datetime import datetime
import json

WEBHOOK_CATCHER_URL = os.getenv("WEBHOOK_CATCHER_URL")

app = FastAPI(title="Test Bot Service - Complete")

@app.get("/")
def root():
    """Root endpoint - now available!"""
    webhook_status = "✅ Connected" if WEBHOOK_CATCHER_URL else "❌ Not configured"
    domain = os.getenv('RAILWAY_PUBLIC_DOMAIN', 'localhost:8000')
    
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
            .endpoint {{ background: #e9ecef; padding: 0.5rem; margin: 0.5rem 0; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <h1>🤖 Test Bot Service</h1>
        <p>Bot is running and ready to receive webhooks!</p>
        
        <div class="status {'connected' if WEBHOOK_CATCHER_URL else 'disconnected'}">
            <strong>Webhook Catcher:</strong> {webhook_status}<br>
            <strong>URL:</strong> {WEBHOOK_CATCHER_URL or 'Not set'}
        </div>
        
        <h3>📡 Available Endpoints:</h3>
        <div class="endpoint"><strong>GET</strong> <code>/</code> - This page</div>
        <div class="endpoint"><strong>GET</strong> <code>/health</code> - Health check</div>
        <div class="endpoint"><strong>POST</strong> <code>/webhook</code> - Receive webhooks</div>
        
        <h3>🧪 Test with cURL (Windows PowerShell):</h3>
        <pre>curl -X POST https://{domain}/webhook -H "Content-Type: application/json" -d '{{"event": "test", "message": "Hello Bot!"}}'</pre>
        
        <h3>🔍 Health Check:</h3>
        <pre>curl https://{domain}/health</pre>
        
        <p><strong>Status:</strong> {'✅ Ready to receive and forward webhooks!' if WEBHOOK_CATCHER_URL else '❌ Set WEBHOOK_CATCHER_URL to enable forwarding.'}</p>
    </body>
    </html>
    """)

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
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "test-bot-complete",
        "version": "3.0-with-root-endpoint",
        "webhook_catcher_configured": bool(WEBHOOK_CATCHER_URL),
        "webhook_catcher_url": WEBHOOK_CATCHER_URL,
        "forwarding_working": bool(WEBHOOK_CATCHER_URL),
        "timestamp": datetime.now().isoformat(),
        "message": "All endpoints working! 🎉"
    }

if __name__ == "__main__":
    uvicorn.run("test:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
