from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from utils.api_client import StockAPI
from utils.chart_generator import ChartGenerator
import os
import requests
import json
from config import HUGGINGFACE_API_KEY

class CommandHandlers:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message:
            return

        help_text = """
📈 *Universal Stock Bot* 📉

Supports all international stocks + AI‑based sentiment analysis!

💡 Examples:
/stock AAPL    → Apple Inc. fiyat bilgisi
/analyze AAPL  → Apple Inc. duygu analizi

✨ Just type /stock SYMBOL or /analyze SYMBOL
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    @staticmethod
    async def stock_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not context.args:
            if update.message:
                await update.message.reply_text(
                    "❌ Please enter a stock symbol. Example: /stock AAPL"
                )
            return

        symbol = context.args[0].upper().strip()
        try:
            data = StockAPI.get_quote(symbol)
            if not data.get('valid'):
                await update.message.reply_text(
                    f"❌ Invalid stock symbol or API error: {data.get('error', 'Unknown error')}"
                )
                return

            chart_path = ChartGenerator.create_stock_chart(symbol, data)
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
                await update.message.reply_photo(photo=open(chart_path, 'rb'),
                                                 caption=f"{symbol} Daily Performance")
                os.remove(chart_path)

        except Exception as e:
            print(f"stock_query error: {e}")
            if update.message:
                await update.message.reply_text("⚠️ An error occurred. Please try again later.")

    @staticmethod
    async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not context.args:
            await update.message.reply_text(
                "🔍 Lütfen bir hisse senedi sembolü girin. Örnek: /analyze AAPL"
            )
            return

        symbol = context.args[0].upper().strip()
        await update.message.reply_text(
            "🤖 Yapay zekâ (FinBERT) analiz ediliyor, lütfen bekleyin..."
        )

        try:
            data = StockAPI.get_quote(symbol)
            if not data.get("valid"):
                await update.message.reply_text(
                    f"❌ Geçersiz sembol veya API hatası: {data.get('error', 'Unknown error')}"
                )
                return

            prompt = (
                f"{symbol} stock update: current=${data['current']}, "
                f"open=${data['open']}, high=${data['high']}, low=${data['low']}. "
                f"Overall sentiment?"
            )

            sentiment, score = await CommandHandlers.query_finbert(prompt)
            if sentiment == "ERROR":
                await update.message.reply_text(f"❌ AI error: {score}")
            else:
                await update.message.reply_text(
                    f"📊 *Sentiment:* {sentiment}\n"
                    f"🎯 *Confidence:* %{round(score * 100, 2)}",
                    parse_mode="Markdown"
                )

        except Exception as e:
            print(f"analyze error: {e}")
            await update.message.reply_text(
                "⚠️ Bir hata oluştu. Lütfen daha sonra tekrar deneyin."
            )

    @staticmethod
    async def query_finbert(prompt: str) -> tuple[str, float]:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": prompt}
        model_url = "https://api-inference.huggingface.co/models/ProsusAI/finbert"

        try:
            resp = requests.post(model_url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()

            # DEBUG
            print("🔥 FinBERT raw response type:", type(result))
            print("🔥 FinBERT raw response content:", json.dumps(result, indent=2))

            # Error dict
            if isinstance(result, dict) and result.get("error"):
                return ("ERROR", result["error"])

            # Handle list formats
            if isinstance(result, list):
                # Nested list format
                if result and isinstance(result[0], list) and result[0]:
                    item = result[0][0]
                # Flat list format
                elif result and isinstance(result[0], dict):
                    item = result[0]
                else:
                    return ("UNKNOWN", 0.0)
            else:
                return ("UNKNOWN", 0.0)

            label = item.get("label", "UNKNOWN").upper()
            score = item.get("score", 0.0)
            return (label, score)

        except Exception as e:
            print(f"🚨 query_finbert hata: {e}")
            return ("ERROR", str(e))
