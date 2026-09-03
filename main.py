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

# Direct MP4 animated video links (100% supported by Telegram)
CAT_GIFS = [
    "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4",
    "https://v.ftcdn.net/03/48/28/73/700_F_348287313_hN37WwKxP0R38Lp7m1Q0m519l99x9e5Y_ST.mp4"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! 🐾\nTimer set korte `/task <minute> <name>` ba `/sec <second> <name>` likhun."
    )

async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutes = float(context.args[0])
        task_name = " ".join(context.args[1:]) if len(context.args) > 1 else "Kaj"
        await update.message.reply_text(f"Timer set! 🐈 '{task_name}'-er jonno {minutes} minute por animated cat alert dibe.")
        
        await asyncio.sleep(minutes * 60)
        
        try:
            gif_url = random.choice(CAT_GIFS)
            await update.message.reply_animation(
                animation=gif_url,
                caption=f"MEOW! 🐱 Apnar '{task_name}' setup korar {minutes} minute somoy par hoye geche!"
            )
        except Exception:
            # Animation send na hole direct text message pathabe
            await update.message.reply_text(f"⏰ ALERT! 🐱 Apnar '{task_name}' setup korar {minutes} minute somoy par hoye geche!")
            
    except (IndexError, ValueError):
        await update.message.reply_text("Sothik bhabe likhun: `/task <minute> <kajer_naam>`")

async def set_sec_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        seconds = float(context.args[0])
        task_name = " ".join(context.args[1:]) if len(context.args) > 1 else "Kaj"
        await update.message.reply_text(f"Timer set! 🐈 '{task_name}'-er jonno {seconds} second por animated cat alert dibe.")
        
        await asyncio.sleep(seconds)
        
        try:
            gif_url = random.choice(CAT_GIFS)
            await update.message.reply_animation(
                animation=gif_url,
                caption=f"MEOW! 🐱 Apnar '{task_name}' setup korar {seconds} second somoy par hoye geche!"
            )
        except Exception:
            # Animation send na hole direct text message pathabe
            await update.message.reply_text(f"⏰ ALERT! 🐱 Apnar '{task_name}' setup korar {seconds} second somoy par hoye geche!")
            
    except (IndexError, ValueError):
        await update.message.reply_text("Sothik bhabe likhun: `/sec <second> <kajer_naam>`")

if __name__ == "__main__":
    threading.Thread(target=run_dummy_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", set_timer))
    app.add_handler(CommandHandler("sec", set_sec_timer))
    print("Bot active hoyeche...")
    app.run_polling()
    
