import os
import sys
import subprocess
import hashlib

print("=" * 50)
print("DSxMODS HWID PROTECTED BOT")
print("=" * 50)

# HWID Key from environment
HWID_KEY = os.getenv('HWID_KEY', 'd2b0ac3c48a5641ccfe2fcd2a2b4d0f947b19f378e8514018306395858e0e3cb')
print(f"HWID Key: {HWID_KEY[:16]}...")

# List files
print("\nFiles in directory:")
for file in os.listdir('.'):
    print(f"  - {file}")

# Check for executables
if os.path.exists("dsxmods.exe"):
    print("\n✅ dsxmods.exe found!")
    print("Attempting to run...")
    
    # Try to run the executable
    try:
        result = subprocess.run(["./dsxmods.exe"], capture_output=True, text=True, timeout=10)
        print("Output:", result.stdout[:500])
    except Exception as e:
        print(f"Error running exe: {e}")
        
elif os.path.exists("DSxMODS_4_2.bin"):
    print("\n✅ DSxMODS_4_2.bin found!")
    print("This is an encrypted binary file.")
    
else:
    print("\n❌ No executable files found!")

# Keep the service alive
print("\n" + "=" * 50)
print("Service is running...")
print("Press Ctrl+C to stop")
print("=" * 50)

# Simple HTTP server to keep alive
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <h1>DSxMODS Bot Active</h1>
    <p>HWID: {HWID_KEY[:16]}...</p>
    <p>Status: ✅ Running</p>
    """

if __name__ == "__main__":
    # Start Flask in background
    import threading
    def run_flask():
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            import time
            time.sleep(60)
            print("[Heartbeat] Service still running...")
    except KeyboardInterrupt:
        print("\nService stopped.")
