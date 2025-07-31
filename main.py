"""
Simple Bot Service for Testing Webhook Integration
================================================

This creates a basic web service that acts like a bot and can receive webhooks.
Deploy this to your bot Railway service (e-production-11c1.up.railway.app).
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import json
import os
import httpx
from datetime import datetime

app = FastAPI(title="Test Bot Service")

# Optional: Send events to webhook catcher
WEBHOOK_CATCHER_URL = os.getenv("WEBHOOK_CATCHER_URL")

@app.get("/")
async def home():
    """Bot service home page"""
    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "localhost:8000")
    webhook_status = "✅ Connected" if WEBHOOK_CATCHER_URL else "❌ Not connected"
    webhook_url = WEBHOOK_CATCHER_URL or "Not configured"
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
            .card { background: #f5f5f5; padding: 1.5rem; margin: 1rem 0; border-radius: 8px; }
            button { background: #007bff; color: white; padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .status { padding: 0.5rem; margin: 0.5rem 0; border-radius: 4px; }800px; margin: 0 auto; }}
            .success { background: #d4edda; color: #155724; }rgin: 1rem 0; border-radius: 8px; }}
            .error { background: #f8d7da; color: #721c24; }dding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; margin: 0.25rem; }}
        </style>on:hover {{ background: #0056b3; }}
    </head> .status {{ padding: 0.5rem; margin: 0.5rem 0; border-radius: 4px; }}
    <body>  .success {{ background: #d4edda; color: #155724; }}
        <h1>🤖 Test Bot Service</h1>8d7da; color: #721c24; }}
        <p>This is your bot service running at: <strong>""" + str(os.getenv("RAILWAY_PUBLIC_DOMAIN", "localhost")) + """</strong></p>
            code {{ font-family: monospace; }}
        <div class="card">
            <h3>Configuration</h3>
            <p><strong>Webhook Catcher URL:</strong> """ + (WEBHOOK_CATCHER_URL or "Not configured") + """</p>
            <p><strong>Status:</strong> """ + ("✅ Connected" if WEBHOOK_CATCHER_URL else "❌ Not connected") + """</p>
        </div>s is your bot service running at: <strong>{domain}</strong></p>
        
        <div class="card">
            <h3>Test Webhook Reception</h3>
            <p>Send a POST request to <code>/webhook</code> to test webhook reception:</p>
            <pre>curl -X POST """ + str(os.getenv("RAILWAY_PUBLIC_DOMAIN", "localhost")) + """/webhook -H "Content-Type: application/json" -d '{"test": "message"}'</pre>
            <button onclick="testWebhook()">🧪 Send Test Webhook</button>
            <div id="result"></div>
        </div>lass="card">
            <h3>🧪 Test Webhook Reception</h3>
        <div class="card"> request to <code>/webhook</code> to test webhook reception:</p>
            <h3>Bot Actions</h3>OST https://{domain}/webhook \\
            <button onclick="simulateBotAction('user_message')">📨 Simulate User Message</button>
            <button onclick="simulateBotAction('command')">⚡ Simulate Command</button>
            <button onclick="simulateBotAction('error')">❌ Simulate Error</button>
        </div>iv id="result"></div>
        </div>
        <script>
            async function testWebhook() {
                const result = document.getElementById('result');
                try {te bot actions (these will be logged to webhook catcher if configured):</p>
                    const response = await fetch('/webhook', {">📨 User Message</button>
                        method: 'POST',tAction('command')">⚡ Command</button>
                        headers: {'Content-Type': 'application/json'},on>
                        body: JSON.stringify({
                            event: 'test_webhook',
                            timestamp: new Date().toISOString(),
                            source: 'bot_interface'
                        })lt = document.getElementById('result');
                    });innerHTML = '<div class="status">⏳ Sending...</div>';
                    const data = await response.json();
                    result.innerHTML = '<div class="status success">✅ Webhook sent successfully!</div>';
                } catch (error) {e = await fetch('/webhook', {{
                    result.innerHTML = '<div class="status error">❌ Error: ' + error.message + '</div>';
                }       headers: {{'Content-Type': 'application/json'}},
            }           body: JSON.stringify({{
                            event: 'test_webhook',
            async function simulateBotAction(type) {ISOString(),
                const result = document.getElementById('result');
                const actions = {ge: 'Test webhook from bot interface'
                    user_message: {
                        event: 'user_message',
                        data: {user_id: 'user_123', message: 'Hello bot!', platform: 'test'}
                    },nst data = await response.json();
                    command: {erHTML = '<div class="status success">✅ Webhook received successfully!</div>';
                        event: 'command_executed',
                        data: {command: '/help', user_id: 'user_123', success: true}.message + '</div>';
                    },
                    error: {
                        event: 'bot_error',
                        data: {error: 'Simulated error', severity: 'warning'}
                    } result = document.getElementById('result');
                };sult.innerHTML = '<div class="status">⏳ Processing...</div>';
                
                try { actions = {{
                    const response = await fetch('/bot-action', {
                        method: 'POST',ssage',
                        headers: {'Content-Type': 'application/json'},ot!', platform: 'test'}}
                        body: JSON.stringify(actions[type])
                    });mand: {{
                    const data = await response.json();
                    result.innerHTML = '<div class="status success">✅ Bot action simulated!</div>';
                } catch (error) {
                    result.innerHTML = '<div class="status error">❌ Error: ' + error.message + '</div>';
                }       event: 'bot_error',
            }           data: {{error: 'Simulated error', severity: 'warning'}}
        </script>   }}
    </body>     }};
    </html>     
    """)        try {{
                    const response = await fetch('/bot-action', {{
@app.post("/webhook")   method: 'POST',
async def receive_webhook(request: Request):Type': 'application/json'}},
    """Receive webhooks (like from other services)"""type])
    try:            }});
        body = await request.body()
        headers = dict(request.headers)response.json();
                    const loggedText = data.logged_to_catcher ? ' (logged to webhook catcher)' : '';
        print(f"Bot received webhook: {body.decode()}")tus success">✅ Bot action simulated!' + loggedText + '</div>';
                }} catch (error) {{
        return {    result.innerHTML = '<div class="status error">❌ Error: ' + error.message + '</div>';
            "status": "received",
            "message": "Webhook processed by bot service",
            "timestamp": datetime.now().isoformat()
        }y>
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bot-action")
async def bot_action(request: Request):est):
    """Simulate bot actions and optionally log to webhook catcher"""
    try:
        data = await request.json()
        headers = dict(request.headers)
        # Simulate bot processing
        print(f"Bot processing: {data}") {body.decode()}")
        print(f"🤖 Headers: {headers}")
        # Optional: Send to webhook catcher for logging
        if WEBHOOK_CATCHER_URL:
            try:tus": "received",
                async with httpx.AsyncClient(timeout=5.0) as client:
                    await client.post().isoformat(),
                        WEBHOOK_CATCHER_URL,
                        json={        }
                            **data,    except Exception as e:
                            "timestamp": datetime.now().isoformat(),        print(f"❌ Error processing webhook: {str(e)}")
                            "source": "bot-service"        raise HTTPException(status_code=500, detail=str(e))
                        }
                    )@app.post("/bot-action")
                    print(f"Logged to webhook catcher: {data['event']}")async def bot_action(request: Request):
                except Exception as e:    """Simulate bot actions and optionally log to webhook catcher"""
                    print(f"Failed to log to webhook catcher: {e}")    try:
                data = await request.json()
        return {        
            "status": "processed",        # Simulate bot processing
            "event": data.get("event"),        print(f"🤖 Bot processing: {data}")
            "logged_to_catcher": bool(WEBHOOK_CATCHER_URL),        
            "timestamp": datetime.now().isoformat()        # Optional: Send to webhook catcher for logging
        }        logged_to_catcher = False
    except Exception as e:        if WEBHOOK_CATCHER_URL:
        raise HTTPException(status_code=500, detail=str(e))            try:
                payload = {
@app.get("/health")                    **data,
async def health():                    "timestamp": datetime.now().isoformat(),
    """Health check endpoint"""                    "source": "bot-service"
    return {                }
        "status": "healthy",                
        "service": "bot",                async with httpx.AsyncClient(timeout=5.0) as client:
        "webhook_catcher_configured": bool(WEBHOOK_CATCHER_URL),                    response = await client.post(
        "timestamp": datetime.now().isoformat()                        WEBHOOK_CATCHER_URL,
    }                        json=payload,
                        headers={"Content-Type": "application/json"}
if __name__ == "__main__":                    )
    import uvicorn                    
    port = int(os.getenv("PORT", 8000))                print(f"✅ Logged to webhook catcher: {data.get('event')} (Status: {response.status_code})")
    uvicorn.run(app, host="0.0.0.0", port=port)                logged_to_catcher = True
```                
requirements.txt            except Exception as e:
```
fastapi==0.104.1
uvicorn==0.24.0     return {
httpx==0.25.2tus": "processed",
```ent": data.get("event"),
        }
        
    except Exception as e:
        print(f"❌ Error in bot action: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "bot",
        "webhook_catcher_configured": bool(WEBHOOK_CATCHER_URL),
        "webhook_catcher_url": WEBHOOK_CATCHER_URL,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```
requirements.txt
```
fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.2
```
