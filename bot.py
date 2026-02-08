import os

print("=" * 50)
print("🤖 DSxMODS BOT - SIMPLE TEST")
print("=" * 50)

HWID_KEY = "d2b0ac3c48a5641ccfe2fcd2a2b4d0f947b19f378e8514018306395858e0e3cb"
BOT_TOKEN = "7361354152:AAFPJRz4gYH1s3JuNVNOogUFvvSTdVsJPYE"
CHAT_ID = "814856314"

print(f"HWID: {HWID_KEY[:16]}...")
print(f"Bot Token: {BOT_TOKEN[:10]}...")
print(f"Chat ID: {CHAT_ID}")

# Check files
import os
print("\n📁 Files in directory:")
for f in os.listdir('.'):
    print(f"  - {f}")

# Simple Flask server to keep alive
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <h1>DSxMODS Bot</h1>
    <p>HWID: {HWID_KEY[:16]}...</p>
    <p>Status: ✅ Simple test running</p>
    """

print("\n✅ Starting Flask server...")
print("✅ Service will stay alive")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
