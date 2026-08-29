import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8641729716:AAHb_S0pT0oLIVyNiIieRtamANVZ_Ho2c-g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Kaj shuru korte `/task <minute> <kajer_naam>` likhun.\n"
        "Example: `/task 30 Setup Work`"
    )

async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutes = int(context.args[0])
        task_name = " ".join(context.args[1:]) if len(context.args) > 1 else "Kaj"
        
        await update.message.reply_text(f"Timer set kora hoyeche! '{task_name}'-er jonno {minutes} minute por alert dewa hobe.")
        
        await asyncio.sleep(minutes * 60)
        
        await update.message.reply_text(f"ALERT! Apnar '{task_name}' setup korar nirdharito {minutes} minute somoy par hoye geche!")
        
    except (IndexError, ValueError):
        await update.message.reply_text("Sothik bhabe likhun: `/task <minute> <kajer_naam>`")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", set_timer))
    
    print("Bot active hoyeche...")
    app.run_polling()
  
