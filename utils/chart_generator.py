import pandas as pd
import matplotlib.pyplot as plt
from config import TIMEOUT

class ChartGenerator:
    @staticmethod
    def create_stock_chart(symbol, data):
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