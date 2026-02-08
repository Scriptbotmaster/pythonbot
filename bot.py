import os
import telebot
from flask import Flask
import threading
import subprocess
import shutil
from datetime import datetime
import zipfile

# ================= CONFIG =================
HWID_KEY = "d2b0ac3c48a5641ccfe2fcd2a2b4d0f947b19f378e8514018306395858e0e3cb"
BOT_TOKEN = "7361354152:AAFPJRz4gYH1s3JuNVNOogUFvvSTdVsJPYE"
CHAT_ID = "814856314"

# Create necessary folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)
os.makedirs("temp", exist_ok=True)

print("=" * 60)
print("🤖 DSxMODS PAK TOOL BOT")
print("=" * 60)
print(f"🔑 HWID: {HWID_KEY[:16]}...")
print(f"📂 Uploads folder: {os.path.abspath('uploads')}")
print(f"📂 Processed folder: {os.path.abspath('processed')}")

# ================= TELEGRAM BOT =================
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
f"""🎮 *DSxMODS PAK Tool Bot*

*BGMI/PUBG .pak File Processor*

🔧 *Features:*
• Extract .pak files (UNPAK)
• Rebuild .pak files (REPAK)
• Clear temporary files
• Direct exe execution

📁 *How to use:*
1. Send me a .pak file
2. I'll process it
3. Download processed file

⚡ *Commands:*
/unpak - Extract .pak file
/repak - Rebuild .pak file
/clear - Clear temp files
/status - Check bot status
/runexe - Run dsxmods.exe directly

🔐 *HWID Verified: {HWID_KEY[:8]}...*""", parse_mode='Markdown')

@bot.message_handler(commands=['unpak'])
def handle_unpak(message):
    bot.reply_to(message, "📤 Please send me a .pak file to extract")
    bot.register_next_step_handler(message, process_unpak)

def process_unpak(message):
    try:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            filename = message.document.file_name
            filepath = f"uploads/{filename}"
            
            with open(filepath, 'wb') as f:
                f.write(downloaded_file)
            
            bot.reply_to(message, f"✅ File received: {filename}\n⏳ Processing UNPAK...")
            
            # Run dsxmods.exe with UNPAK option
            process = subprocess.Popen(
                ["./dsxmods.exe"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send '1' for UNPAK option
            output, error = process.communicate(input='1\n')
            
            if process.returncode == 0:
                # Find extracted files
                extracted_folder = "Unpacked_PAK"
                if os.path.exists(extracted_folder):
                    # Create zip of extracted files
                    zip_filename = f"processed/{filename}_unpacked.zip"
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        for root, dirs, files in os.walk(extracted_folder):
                            for file in files:
                                zipf.write(os.path.join(root, file))
                    
                    # Send zip file
                    with open(zip_filename, 'rb') as zipf:
                        bot.send_document(message.chat.id, zipf, caption=f"✅ {filename} extracted successfully!")
                else:
                    bot.reply_to(message, "❌ Extraction failed. No output folder found.")
            else:
                bot.reply_to_message(message, f"❌ Error: {error}")
                
    except Exception as e:
        bot.reply_to_message(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['repak'])
def handle_repak(message):
    bot.reply_to(message, "📤 Please send me extracted files as ZIP")
    bot.register_next_step_handler(message, process_repak)

def process_repak(message):
    try:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            filename = message.document.file_name
            filepath = f"uploads/{filename}"
            
            with open(filepath, 'wb') as f:
                f.write(downloaded_file)
            
            bot.reply_to_message(message, f"✅ File received: {filename}\n⏳ Processing REPAK...")
            
            # Extract ZIP first
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall("temp/extracted")
            
            # Run dsxmods.exe with REPAK option
            process = subprocess.Popen(
                ["./dsxmods.exe"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send '2' for REPAK option
            output, error = process.communicate(input='2\n')
            
            if process.returncode == 0:
                # Find repacked file
                for file in os.listdir('.'):
                    if file.endswith('.pak'):
                        with open(file, 'rb') as f:
                            bot.send_document(message.chat.id, f, caption=f"✅ Repacked: {file}")
                        break
                else:
                    bot.reply_to_message(message, "❌ No .pak file generated")
            else:
                bot.reply_to_message(message, f"❌ Error: {error}")
                
    except Exception as e:
        bot.reply_to_message(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['clear'])
def handle_clear(message):
    try:
        # Run dsxmods.exe with CLEAR option
        process = subprocess.Popen(
            ["./dsxmods.exe"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        output, error = process.communicate(input='3\n')
        bot.reply_to_message(message, "✅ All temporary files cleared!")
        
    except Exception as e:
        bot.reply_to_message(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['runexe'])
def handle_runexe(message):
    try:
        bot.reply_to_message(message, "🚀 Running dsxmods.exe...")
        
        # Direct run with subprocess
        process = subprocess.run(
            ["./dsxmods.exe"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = process.stdout[:2000]  # Limit output
        bot.reply_to_message(message, f"📟 *Output:*\n```\n{output}\n```", parse_mode='Markdown')
        
    except subprocess.TimeoutExpired:
        bot.reply_to_message(message, "⏱️ Process timed out (30s)")
    except Exception as e:
        bot.reply_to_message(message, f"❌ Error: {str(e)}")

@bot.message_handler(commands=['status'])
def handle_status(message):
    files = os.listdir('.')
    pak_files = [f for f in files if f.endswith('.pak')]
    
    status_msg = f"""📊 *Bot Status:*
✅ Server: Active
🤖 Telegram: Connected
🔑 HWID: Verified
📁 Files: {len(files)}
.pak files: {len(pak_files)}
🕒 Time: {datetime.now().strftime('%H:%M:%S')}
🌐 URL: https://pythonbot-p0wz.onrender.com"""
    
    bot.reply_to_message(message, status_msg, parse_mode='Markdown')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document.file_name.endswith('.pak'):
        handle_unpak(message)
    elif message.document.file_name.endswith('.zip'):
        handle_repak(message)
    else:
        bot.reply_to_message(message, "❌ Please send .pak or .zip files only")

# ================= WEB INTERFACE =================
app = Flask(__name__)

@app.route('/')
def home():
    files = os.listdir('.')
    pak_files = [f for f in files if f.endswith('.pak')]
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DSxMODS PAK Tool</title>
        <style>
            body {{ font-family: Arial; background: #0f0f23; color: #0f0; padding: 20px; }}
            .container {{ max-width: 900px; margin: auto; background: #1a1a2e; padding: 30px; border-radius: 10px; }}
            h1 {{ color: #00ff00; border-bottom: 2px solid #00ff00; }}
            .file-list {{ background: #16213e; padding: 15px; border-radius: 5px; }}
            .command {{ background: #0f3460; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 DSxMODS PAK Tool Server</h1>
            <p>HWID: <code>{HWID_KEY[:24]}...</code></p>
            
            <div class="command">
                <h3>📁 Available Files:</h3>
                <pre>{'\\n'.join(files[:20])}</pre>
            </div>
            
            <div class="command">
                <h3>🎮 .pak Files Found: {len(pak_files)}</h3>
                {'<br>'.join(pak_files)}
            </div>
            
            <div class="command">
                <h3>📲 Telegram Bot Commands:</h3>
                /start - Show help<br>
                /unpak - Extract .pak file<br>
                /repak - Rebuild .pak file<br>
                /clear - Clear temp files<br>
                /runexe - Run tool directly<br>
                /status - Check status
            </div>
            
            <p>👉 <a href="https://t.me/dsxmods_bot" style="color: #00ff00;">Open Telegram Bot</a></p>
        </div>
    </body>
    </html>
    """

# ================= START SERVERS =================
def run_flask():
    print("🌐 Starting web interface...")
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

def run_telegram_bot():
    print("🤖 Starting Telegram bot...")
    try:
        bot.send_message(CHAT_ID, 
f"""🚀 *DSxMODS PAK Tool Started!*

✅ Server: Render.com
🔑 HWID: `{HWID_KEY[:16]}...`
📁 Files ready for processing
🎮 BGMI/PUBG .pak tool active

Send .pak files to extract or use commands!""", parse_mode='Markdown')
    except:
        print("⚠️ Could not send startup message")
    
    print("✅ Bot polling started")
    bot.infinity_polling()

if __name__ == "__main__":
    # Start web server
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start Telegram bot
    run_telegram_bot()
