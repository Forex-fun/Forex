import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor
import requests

class MarketDataFetcher:
    def __init__(self):
        self.cache = {}
        self.logger = logging.getLogger(__name__)
        
    def fetch_historical_data(self, symbol, period='1y', interval='1d'):
        try:
            # Check cache first
            cache_key = f"{symbol}_{period}_{interval}"
            if cache_key in self.cache:
                if datetime.now() - self.cache[cache_key]['timestamp'] < timedelta(hours=1):
                    return self.cache[cache_key]['data']
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            # Process and clean the data
            data = self._process_data(data)
            
            # Add to cache
            self.cache[cache_key] = {
                'data': data,
                'timestamp': datetime.now()
            }
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise
    
    def _process_data(self, data):
        # Remove missing values
        data = data.dropna()
        
        # Calculate technical indicators
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['RSI'] = self._calculate_rsi(data['Close'])
        
        # Add volatility indicator
        data['Volatility'] = data['Close'].rolling(window=20).std()
        
        # Add trading volume moving average
        data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
        
        # Add price momentum
        data['Price_Momentum'] = data['Close'].pct_change(periods=5)
        
        return data.fillna(0)
    
    def _calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def fetch_multiple_symbols(self, symbols, period='1y', interval='1d'):
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = {}
            future_to_symbol = {
                executor.submit(self.fetch_historical_data, symbol, period, interval): symbol 
                for symbol in symbols
            }
            
            for future in future_to_symbol:
                symbol = future_to_symbol[future]
                try:
                    results[symbol] = future.result()
                except Exception as e:
                    self.logger.error(f"Error fetching {symbol}: {str(e)}")
                    
            return results 