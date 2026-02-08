import os
import telebot
from flask import Flask
import threading

# ================= CONFIG =================
HWID_KEY = "d2b0ac3c48a5641ccfe2fcd2a2b4d0f947b19f378e8514018306395858e0e3cb"
BOT_TOKEN = "7361354152:AAFPJRz4gYH1s3JuNVNOogUFvvSTdVsJPYE"
CHAT_ID = "814856314"

print("=" * 60)
print("🤖 DSxMODS TELEGRAM BOT v2.0")
print("=" * 60)
print(f"🔑 HWID: {HWID_KEY[:16]}...")
print(f"🤖 Bot Token: {BOT_TOKEN[:15]}...")
print(f"👤 Chat ID: {CHAT_ID}")

# ================= TELEGRAM BOT =================
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 
f"""✅ *DSxMODS Bot Active!*

*Your ID:* {message.from_user.id}
*HWID:* `{HWID_KEY[:16]}...`

*Commands:*
/start - Start bot
/hwid - Show full HWID
/status - Bot status
/files - List server files
/url - Get bot URL""", parse_mode='Markdown')

@bot.message_handler(commands=['hwid'])
def show_hwid(message):
    bot.reply_to_message(message, 
f"""🔐 *FULL HWID KEY:*
`{HWID_KEY}`""", parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to_message(message,
"""📊 *BOT STATUS:*
✅ Server: Live on Render
🤖 Telegram: Connected
🔑 HWID: Verified
🌐 URL: https://pythonbot-p0wz.onrender.com
🕒 Uptime: 24/7""", parse_mode='Markdown')

@bot.message_handler(commands=['files'])
def list_files(message):
    files = os.listdir('.')
    file_list = "\n".join([f"📄 {f}" for f in files[:10]])
    bot.reply_to_message(message, 
f"""📁 *Server Files:*
{file_list}

Total: {len(files)} files""", parse_mode='Markdown')

@bot.message_handler(commands=['url'])
def send_url(message):
    bot.reply_to_message(message,
f"""🌐 *Bot Web Interface:*
https://pythonbot-p0wz.onrender.com

🔑 *HWID Verification Page*
Always active!""", parse_mode='Markdown')

# ================= WEB SERVER =================
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DSxMODS Bot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 800px;
                margin: 50px auto;
                background: rgba(0, 0, 0, 0.7);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            h1 {{
                color: #4CAF50;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 10px;
            }}
            .status {{
                color: #4CAF50;
                font-weight: bold;
                font-size: 1.2em;
            }}
            .hwid {{
                background: #1a1a1a;
                padding: 10px;
                border-radius: 5px;
                font-family: monospace;
                word-break: break-all;
                margin: 10px 0;
            }}
            .button {{
                display: inline-block;
                background: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                margin: 10px 5px;
                transition: 0.3s;
            }}
            .button:hover {{
                background: #45a049;
                transform: translateY(-2px);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 DSxMODS Bot Control Panel</h1>
            <p class="status">✅ Status: LIVE & ACTIVE</p>
            
            <h2>🔑 HWID Verification</h2>
            <div class="hwid">{HWID_KEY}</div>
            
            <h2>📊 Bot Information</h2>
            <p><strong>Telegram Bot:</strong> @DSxMODS_Bot</p>
            <p><strong>Chat ID:</strong> {CHAT_ID}</p>
            <p><strong>Server:</strong> Render.com (24/7)</p>
            
            <h2>🚀 Quick Actions</h2>
            <a href="https://t.me/dsxmods_bot" class="button" target="_blank">Open Telegram Bot</a>
            <a href="https://github.com/Scriptbotmaster/pythonbot" class="button" target="_blank">View Source Code</a>
            
            <h2>📈 System Status</h2>
            <p>• HWID Verification: ✅ ACTIVE</p>
            <p>• Telegram Connection: ✅ ONLINE</p>
            <p>• Server Uptime: 24/7</p>
            <p>• Last Update: {os.popen('date').read().strip()}</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

@app.route('/hwid')
def hwid_api():
    return {{"hwid": HWID_KEY, "status": "verified"}}

# ================= START BOTH SERVERS =================
def run_flask():
    print("🌐 Starting Flask server on port 8080...")
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def run_telegram_bot():
    print("🤖 Starting Telegram bot polling...")
    try:
        # Send startup notification
        bot.send_message(CHAT_ID,
f"""🚀 *DSxMODS Bot Restarted Successfully!*

*Server:* Render.com
*URL:* https://pythonbot-p0wz.onrender.com
*HWID:* `{HWID_KEY[:16]}...`
*Status:* 🟢 24/7 Active""", parse_mode='Markdown')
        print("✅ Startup message sent to Telegram")
    except Exception as e:
        print(f"⚠️ Telegram notification failed: {e}")
    
    # Start bot polling
    bot.infinity_polling()

if __name__ == "__main__":
    # Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start Telegram bot in main thread
    run_telegram_bot()
