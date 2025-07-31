"""
Simple Test Bot for Webhook Catcher Integration
=============================================

This script simulates a bot that sends various events to the webhook catcher.
Use this to test the forwarding functionality.
"""

import os
import asyncio
import httpx
from datetime import datetime

# Your webhook catcher URL - update this with your actual Railway URL
WEBHOOK_CATCHER_URL = os.getenv("WEBHOOK_CATCHER_URL", "https://test-production-ea66.up.railway.app/webhook")

class TestBot:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.session_id = f"test-session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    async def send_event(self, event_type: str, data: dict):
        """Send an event to the webhook catcher"""
        payload = {
            "event": event_type,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "data": data,
            "source": "test-bot"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "TestBot/1.0",
                        "X-Bot-Type": "test-integration"
                    }
                )
                
            print(f"✅ Sent {event_type}: Status {response.status_code}")
            return response.status_code
            
        except Exception as e:
            print(f"❌ Failed to send {event_type}: {e}")
            return None
    
    async def run_test_sequence(self):
        """Run a sequence of test events"""
        print(f"🚀 Starting test bot session: {self.session_id}")
        print(f"📡 Sending events to: {self.webhook_url}")
        print("-" * 50)
        
        # Test events sequence
        test_events = [
            ("bot_startup", {
                "version": "1.0.0",
                "environment": "test",
                "features": ["webhooks", "logging"]
            }),
            
            ("user_message", {
                "user_id": "user_123",
                "username": "alice",
                "message": "Hello bot!",
                "chat_id": "chat_456"
            }),
            
            ("command_executed", {
                "command": "/help",
                "user_id": "user_123",
                "response_time_ms": 45,
                "success": True
            }),
            
            ("api_call", {
                "endpoint": "/api/weather",
                "method": "GET",
                "status_code": 200,
                "response_time_ms": 120
            }),
            
            ("error_occurred", {
                "error_type": "timeout",
                "message": "API request timed out",
                "severity": "warning",
                "stack_trace": "Simulated error for testing"
            }),
            
            ("user_joined", {
                "user_id": "user_789",
                "username": "bob",
                "invite_code": "abc123",
                "referrer": "alice"
            }),
            
            ("payment_received", {
                "user_id": "user_123",
                "amount": 19.99,
                "currency": "USD",
                "subscription_type": "premium"
            }),
            
            ("bot_shutdown", {
                "uptime_seconds": 3600,
                "events_processed": 150,
                "reason": "maintenance"
            })
        ]
        
        # Send events with delays
        for i, (event_type, data) in enumerate(test_events, 1):
            print(f"[{i}/{len(test_events)}] Sending {event_type}...")
            await self.send_event(event_type, data)
            
            # Wait between events to see them separately
            if i < len(test_events):
                await asyncio.sleep(2)
        
        print("-" * 50)
        print("✅ Test sequence completed!")
        print(f"🔍 Check your webhook catcher at: {self.webhook_url.replace('/webhook', '')}")

async def main():
    # Get webhook URL from environment or use default
    webhook_url = WEBHOOK_CATCHER_URL
    
    if not webhook_url:
        print("❌ Error: WEBHOOK_CATCHER_URL not set!")
        print("Set it with: export WEBHOOK_CATCHER_URL='https://your-app.railway.app/webhook'")
        return
    
    # Ensure URL ends with /webhook
    if not webhook_url.endswith('/webhook'):
        webhook_url = webhook_url.rstrip('/') + '/webhook'
    
    print("🧪 Webhook Catcher Test Bot")
    print("=" * 30)
    
    # Create and run test bot
    bot = TestBot(webhook_url)
    await bot.run_test_sequence()

if __name__ == "__main__":
    asyncio.run(main())
