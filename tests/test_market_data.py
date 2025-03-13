import pytest
from src.data.market_data import MarketDataFetcher
from datetime import datetime, timedelta

@pytest.fixture
def market_data():
    return MarketDataFetcher()

def test_fetch_historical_data(market_data):
    data = market_data.fetch_historical_data('BTC-USD', period='1mo')
    assert not data.empty
    assert all(col in data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])
    assert all(col in data.columns for col in ['SMA_20', 'SMA_50', 'RSI'])

def test_calculate_rsi(market_data):
    data = market_data.fetch_historical_data('ETH-USD', period='1mo')
    rsi = data['RSI']
    assert not rsi.empty
    assert all(0 <= value <= 100 for value in rsi.dropna())

def test_data_caching(market_data):
    # First fetch
    data1 = market_data.fetch_historical_data('BTC-USD', period='1d')
    
    # Second fetch (should be from cache)
    data2 = market_data.fetch_historical_data('BTC-USD', period='1d')
    
    assert data1.equals(data2)

def test_multiple_symbols(market_data):
    symbols = ['BTC-USD', 'ETH-USD']
    results = market_data.fetch_multiple_symbols(symbols)
    
    assert len(results) == len(symbols)
    for symbol in symbols:
        assert symbol in results
        assert not results[symbol].empty 