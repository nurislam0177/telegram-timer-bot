import asyncio
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8641729716:AAHb_S0pT0oLIVyNiIieRtamANVZ_Ho2c-g"

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Kaj shuru korte `/task <minute/second> <kajer_naam>` likhun.\n"
        "Example: `/task 0.5 Quick Test` ba `/sec 30 Quick Test`"
    )

async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # int-er poriborte float use kora hoyeche, jaate 0.5, 1.5 ityadi support kare
        minutes = float(context.args[0])
        task_name = " ".join(context.args[1:]) if len(context.args) > 1 else "Kaj"
        
        await update.message.reply_text(f"Timer set kora hoyeche! '{task_name}'-er jonno {minutes} minute por alert dewa hobe.")
        
        # Total second hiseb kora (0.5 * 60 = 30 seconds)
        await asyncio.sleep(minutes * 60)
        
        await update.message.reply_text(f"ALERT! Apnar '{task_name}' setup korar nirdharito {minutes} minute somoy par hoye geche!")
        
    except (IndexError, ValueError):
        await update.message.reply_text("Sothik bhabe likhun: `/task <minute> <kajer_naam>`\nExample: `/task 0.5 Test`")

# Direct Second-er jonno optional notun command `/sec`
async def set_sec_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        seconds = float(context.args[0])
        task_name = " ".join(context.args[1:]) if len(context.args) > 1 else "Kaj"
        
        await update.message.reply_text(f"Timer set kora hoyeche! '{task_name}'-er jonno {seconds} second por alert dewa hobe.")
        
        await asyncio.sleep(seconds)
        
        await update.message.reply_text(f"ALERT! Apnar '{task_name}' setup korar {seconds} second somoy par hoye geche!")
        
    except (IndexError, ValueError):
        await update.message.reply_text("Sothik bhabe likhun: `/sec <second> <kajer_naam>`\nExample: `/sec 10 Test`")

if __name__ == "__main__":
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", set_timer))
    app.add_handler(CommandHandler("sec", set_sec_timer))
    
    print("Bot active hoyeche...")
    app.run_polling()
        await update.message.reply_text(f"ALERT! Apnar '{task_name}' setup korar nirdharito {minutes} minute somoy par hoye geche!")
        
    except (IndexError, ValueError):
        await update.message.reply_text("Sothik bhabe likhun: `/task <minute> <kajer_naam>`")

if __name__ == "__main__":
    # Start fake web server to satisfy Render
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", set_timer))
    
    print("Bot active hoyeche...")
    app.run_polling()
    
