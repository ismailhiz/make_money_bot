BU KOD ÇALIŞAN BÜTÜN NASDAQ HİSSELERİNİ ÇEKEEN KOD :


import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# API Key'ler
TELEGRAM_TOKEN = ""
FINNHUB_API_KEY = ""

# Finnhub API için header
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_stock_data(symbol):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('c') is None:
            return {'error': 'Stock data not found', 'valid': False}
            
        return {
            'current': data['c'],
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'valid': True
        }
    except Exception as e:
        return {'error': f"API Error: {str(e)}", 'valid': False}

def generate_stock_chart(symbol, data):
    try:
        df = pd.DataFrame({
            'Price': [data['current']],
            'Open': [data['open']],
            'High': [data['high']],
            'Low': [data['low']]
        })
        
        plt.figure(figsize=(10, 6))
        ax = df.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        
        plt.title(f"{symbol} Stock Data ($)", pad=20, fontsize=14)
        plt.xlabel('')
        plt.ylabel('Price ($)', fontsize=12)
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        for p in ax.patches:
            ax.annotate(f"${p.get_height():.2f}", 
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='center', xytext=(0, 10),
                       textcoords='offset points', fontsize=10)
        
        plt.tight_layout()
        chart_path = f"{symbol}_chart.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        return chart_path
    except Exception as e:
        print(f"Chart error: {e}")
        return None

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

async def stock_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not context.args:
        if update.message:
            await update.message.reply_text("❌ Please enter a stock symbol. Example: /stock AAPL")
        return
    
    symbol = context.args[0].upper().strip()
    
    try:
        # Get stock data
        data = get_stock_data(symbol)
        if not data.get('valid'):
            await update.message.reply_text(f"❌ Invalid stock symbol or API error: {data.get('error', 'Unknown error')}")
            return
        
        # Generate chart
        chart_path = generate_stock_chart(symbol, data)
        
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

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stock", stock_query))
    
    print("🤖 Universal Stock Bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()

    BURADA BİTİYOR...




    
