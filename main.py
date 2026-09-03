import asyncio
import os
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# Meow Sound MP3 Links
CAT_SOUNDS = [
    "https://assets.mixkit.co/active_storage/sfx/228/228-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/232/232-preview.mp3"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! 🐾\nCommands:\n"
        "/task <minute> <name> - Timer set\n"
        "/sec <second> <name> - Short timer\n"
        "/myself - About Me\n"
        "/fb - Facebook Link\n"
        "/movie - Movie List"
    )

async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutes = float(context.args[0])
        task_name = " ".join(context.args[1:]) if len(context.args) > 1 else "Kaj"
        await update.message.reply_text(f"Timer set! 🐈 '{task_name}'-er jonno {minutes} minute por sound alert dibe.")
        
        await asyncio.sleep(minutes * 60)
        
        try:
            sound_url = random.choice(CAT_SOUNDS)
            await update.message.reply_audio(
                audio=sound_url,
                caption=f"⏰ MEOW! 🐱 Apnar '{task_name}' setup korar {minutes} minute somoy par hoye geche!"
            )
        except Exception:
            await update.message.reply_text(f"⏰ ALERT! 🐱 Apnar '{task_name}' setup korar {minutes} minute somoy par hoye geche!")
            
    except (IndexError, ValueError):
        await update.message.reply_text("Sothik bhabe likhun: `/task <minute> <kajer_naam>`")

async def set_sec_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        seconds = float(context.args[0])
        task_name = " ".join(context.args[1:]) if len(context.args) > 1 else "Kaj"
        await update.message.reply_text(f"Timer set! 🐈 '{task_name}'-er jonno {seconds} second por sound alert dibe.")
        
        await asyncio.sleep(seconds)
        
        try:
            sound_url = random.choice(CAT_SOUNDS)
            await update.message.reply_audio(
                audio=sound_url,
                caption=f"⏰ MEOW! 🐱 Apnar '{task_name}' setup korar {seconds} second somoy par hoye geche!"
            )
        except Exception:
            await update.message.reply_text(f"⏰ ALERT! 🐱 Apnar '{task_name}' setup korar {seconds} second somoy par hoye geche!")
            
    except (IndexError, ValueError):
        await update.message.reply_text("Sothik bhabe likhun: `/sec <second> <kajer_naam>`")

# Myself Command (/myself)
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম, আমি মোহাম্মদ নূর ইসলাম।")

# Facebook Link Command (/fb)
async def fb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fb_url = "https://www.facebook.com/your_username" 
    await update.message.reply_text(f"📌 Amar Facebook ID Profile Link:\n{fb_url}")

# Movie List Command (/movie)
async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_list = (
        "🍿 **Recommended Movie List:**\n\n"
        "1. Interstellar\n"
        "2. Inception\n"
        "3. The Dark Knight\n"
        "4. Avatar\n"
        "5. Fight Club"
    )
    await update.message.reply_text(movie_list, parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_dummy_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Registering all Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", set_timer))
    app.add_handler(CommandHandler("sec", set_sec_timer))
    app.add_handler(CommandHandler("myself", my_command))
    app.add_handler(CommandHandler("fb", fb_command))
    app.add_handler(CommandHandler("movie", movie_command))
    
    print("Bot active hoyeche...")
    app.run_polling()
    
