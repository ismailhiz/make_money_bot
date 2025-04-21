from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.api_client import StockAPI
from utils.chart_generator import ChartGenerator
import os

class CommandHandlers:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message:
            return
            
        help_text = """
📈 *Universal Stock Bot* 📉

Now supports ALL international stocks!

💡 Examples:
/stock AAPL  → Apple Inc.
/stock TSLA  → Tesla
/stock MSFT  → Microsoft
/stock AMZN  → Amazon

✨ Just type /stock SYMBOL
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    @staticmethod
    async def stock_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not context.args:
            if update.message:
                await update.message.reply_text("❌ Please enter a stock symbol. Example: /stock AAPL")
            return
        
        symbol = context.args[0].upper().strip()
        
        try:
            # Get stock data
            data = StockAPI.get_quote(symbol)
            if not data.get('valid'):
                await update.message.reply_text(f"❌ Invalid stock symbol or API error: {data.get('error', 'Unknown error')}")
                return
            
            # Generate chart
            chart_path = ChartGenerator.create_stock_chart(symbol, data)
            
            # Prepare message
            message = (
                f"📊 *{symbol} Stock Info*\n\n"
                f"• Current: `${data['current']:.2f}`\n"
                f"• Open: `${data['open']:.2f}`\n"
                f"• High: `${data['high']:.2f}`\n"
                f"• Low: `${data['low']:.2f}`\n\n"
                f"⏳ Last update: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
            if chart_path:
                try:
                    await update.message.reply_photo(
                        photo=open(chart_path, 'rb'),
                        caption=f"{symbol} Daily Performance"
                    )
                    os.remove(chart_path)
                except Exception as e:
                    print(f"Failed to send chart: {e}")
                    
        except Exception as e:
            print(f"Error details: {e}")
            if update.message:
                await update.message.reply_text("⚠️ An error occurred. Please try again later.")