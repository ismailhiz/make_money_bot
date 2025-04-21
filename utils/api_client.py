import requests
from config import FINNHUB_API_KEY, HEADERS, TIMEOUT

class StockAPI:
    @staticmethod
    def get_quote(symbol):
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
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