# 📈 Universal Stock Bot 🤖  
**Universal Stock Bot**, uluslararası borsa hisseleri hakkında anlık bilgi sunan ve yapay zekâ (AI) destekli analiz sağlayan gelişmiş bir **Telegram botudur**.  
## 🚀 Özellikler  
- 🔍 `/stock SYMBOL` komutuyla herhangi bir hisse senedinin güncel piyasa verilerini alın.  
- 🤖 `/analyze SYMBOL` komutuyla AI destekli yatırımcı analizine ulaşın.  
- 🧠 Yapay zekâ analizleri FinBERT (finance-specific BERT) modeli ile gerçekleştiriliyor.  
- 📉 Hisse senedine özel günlük performans grafikleri otomatik olarak oluşturulur.  
- 🌍 Tüm dünyadan hisse senetlerini destekler (örnek: AAPL, TSLA, NVDA, MSFT, vb.).  
- ✨ Türkçe ve İngilizce kullanım için uygun yapı.  
## 👨‍💻 Geliştirici  
Bu bot, yazılım geliştirici ve eğitmen **İsmail Hız** tarafından geliştirilmiştir. Kendisi front-end geliştirme, yapay zekâ uygulamaları ve eğitim odaklı projelerde aktif olarak çalışmaktadır. Ücretsiz yazılım eğitimleri sunduğu [Hizzacademy](https://github.com/ismailhiz) platformunun da kurucusudur.  
## 📷 Örnek Kullanım  
```bash  
/stock AAPL  
/analyze TSLA  
```  
Bot size aşağıdaki bilgileri sağlar:  
- ✅ Anlık fiyat  
- 📈 Gün içi en yüksek/düşük değer  
- 🧠 AI ile yorum: "Yatırımcılar dikkatli olmalı", "İyimser olabilir" gibi öneriler  
- 🖼️ Günlük performans grafiği  
## ⚙️ Kullanılan Teknolojiler  
- **Python 3.10+**  
- [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) — Telegram API entegrasyonu  
- [`FinBERT`](https://github.com/ProsusAI/finBERT) — AI destekli duygu analizi  
- `Matplotlib` — Hisse grafiklerinin oluşturulması  
- `requests` — API ile veri çekme  
- `dotenv` — Ortam değişkenlerinin güvenli yönetimi  
## 🧪 Kurulum  
```bash  
# 1. Depoyu klonla  
git clone https://github.com/ismailhiz/universal-stock-bot.git  
cd universal-stock-bot  
  
# 2. Sanal ortam oluştur (isteğe bağlı)  
python -m venv venv  
source venv/bin/activate  
  
# 3. Gerekli kütüphaneleri yükle  
pip install -r requirements.txt  
  
# 4. API anahtarlarını ekle (config.py veya .env üzerinden)  
```  
## 📬 Nasıl Kullanılır?  
1. Telegram’da kendi botunuzu oluşturun: [@BotFather](https://t.me/BotFather)  
2. `TELEGRAM_BOT_TOKEN` anahtarını alın ve config dosyasına ekleyin.  
3. Python dosyasını çalıştırın:  
```bash  
python main.py  
```  
---  
🧠 Geri bildirimler ve katkılarınız için teşekkürler!  
Made with ❤️ by [İsmail Hız](https://github.com/ismailhiz)
