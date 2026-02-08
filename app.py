from flask import Flask
import os

app = Flask(__name__)

HWID_KEY = os.getenv('HWID_KEY', 'd2b0ac3c48a5641ccfe2fcd2a2b4d0f947b19f378e8514018306395858e0e3cb')

@app.route('/')
def home():
    return f"""
    <h1>DSxMODS Bot Active</h1>
    <p>HWID: {HWID_KEY[:16]}...</p>
    <p>Status: ✅ Running</p>
    <p>Service keeps active with HTTP requests</p>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
