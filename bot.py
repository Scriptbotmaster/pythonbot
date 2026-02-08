import os
import telebot
import threading
from flask import Flask

# ================= CONFIGURATION =================
HWID_KEY = "d2b0ac3c48a5641ccfe2fcd2a2b4d0f947b19f378e8514018306395858e0e3cb"
BOT_TOKEN = "7361354152:AAFPJRz4gYH1s3JuNVNOogUFvvSTdVsJPYE"
CHAT_ID = "814856314"

print("=" * 50)
print("🤖 DSxMODS TELEGRAM BOT")
print("=" * 50)
print(f"HWID: {HWID_KEY[:16]}...")
print(f"Bot Token: {BOT_TOKEN[:10]}...")
print(f"Chat ID: {CHAT_ID}")

# ================= TELEGRAM BOT =================
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.from_user
    bot.reply_to(message, 
f"""✅ *DSxMODS Bot Active!*

*User:* {user.first_name} (@{user.username})
*ID:* {user.id}

*HWID:* `{HWID_KEY[:16]}...`
*Status:* 🟢 Running on Render

Commands:
/start - Start bot
/hwid - Show HWID
/files - List files
/status - Check status
/run - Execute program""", parse_mode='Markdown')

@bot.message_handler(commands=['hwid'])
def show_hwid(message):
    bot.reply_to(message, f"🔑 *HWID Key:*\n`{HWID_KEY}`", parse_mode='Markdown')

@bot.message_handler(commands=['files'])
def list_files(message):
    import os
    files = os.listdir('.')
    file_list = "\n".join([f"• {f}" for f in files])
    bot.reply_to(message, f"📁 *Files in server:*\n{file_list}", parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status(message):
    import psutil
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    bot.reply_to(message, 
f"""📊 *System Status:*
CPU: {cpu}%
Memory: {memory}%
Service: 🟢 Active
URL: https://pythonbot-p0wz.onrender.com""", parse_mode='Markdown')

@bot.message_handler(commands=['run'])
def run_exe(message):
    import subprocess
    try:
        if os.path.exists("dsxmods.exe"):
            bot.reply_to(message, "🚀 *Running dsxmods.exe...*", parse_mode='Markdown')
            result = subprocess.run(["./dsxmods.exe"], capture_output=True, text=True, timeout=30)
            output = result.stdout[:1000] or "No output"
            bot.reply_to(message, f"📤 *Output:*\n```\n{output}\n```", parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ *dsxmods.exe not found!*", parse_mode='Markdown')
    except Exception as e:
        bot.reply_to_message(message, f"❌ *Error:* {str(e)}", parse_mode='Markdown')

# ================= WEB SERVER (KEEP ALIVE) =================
app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DSxMODS Bot</title>
        <style>
            body {{ font-family: Arial; padding: 20px; background: #0f0f0f; color: white; }}
            .container {{ max-width: 800px; margin: auto; }}
            .status {{ color: #4CAF50; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 DSxMODS Bot Active</h1>
            <p class="status">✅ Status: Running</p>
            <p>HWID: {HWID_KEY[:16]}...</p>
            <p>Telegram Bot: @{(await bot.get_me()).username}</p>
            <p>Chat ID: {CHAT_ID}</p>
            <hr>
            <p>This service keeps the Telegram bot 24/7 active.</p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

# ================= START EVERYTHING =================
def run_flask():
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def run_bot():
    print("Starting Telegram bot polling...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    print("✅ Flask server started on port 8080")
    print("✅ Telegram bot initializing...")
    
    # Send startup message to Telegram
    try:
        bot.send_message(CHAT_ID, 
f"""🚀 *DSxMODS Bot Started Successfully!*

*Server:* Render.com
*URL:* https://pythonbot-p0wz.onrender.com
*HWID:* `{HWID_KEY[:16]}...`
*Status:* 🟢 Active 24/7""", parse_mode='Markdown')
        print("✅ Startup message sent to Telegram")
    except Exception as e:
        print(f"⚠️ Could not send Telegram message: {e}")
    
    # Start bot polling (main thread)
    run_bot()
