import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.commands import CommandHandlers
from config import TELEGRAM_TOKEN

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", CommandHandlers.start))
    app.add_handler(CommandHandler("stock", CommandHandlers.stock_query))
    
    print("🤖 Universal Stock Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()