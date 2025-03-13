import pytest
import pandas as pd
import numpy as np
from src.models.prediction_model import MarketPredictionModel

@pytest.fixture
def sample_data():
    # Create sample data for testing
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = pd.DataFrame({
        'Open': np.random.uniform(100, 200, len(dates)),
        'High': np.random.uniform(150, 250, len(dates)),
        'Low': np.random.uniform(50, 150, len(dates)),
        'Close': np.random.uniform(100, 200, len(dates)),
        'Volume': np.random.uniform(1000000, 5000000, len(dates))
    }, index=dates)
    
    # Add technical indicators
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['RSI'] = 50 + np.random.uniform(-20, 20, len(dates))
    data['MACD'] = np.random.uniform(-10, 10, len(dates))
    data['Signal_Line'] = np.random.uniform(-10, 10, len(dates))
    
    return data.dropna()

def test_model_initialization():
    model = MarketPredictionModel()
    assert model.model is not None
    assert model.scaler is not None

def test_data_preprocessing(sample_data):
    model = MarketPredictionModel()
    processed_data = model.preprocess_data(sample_data)
    assert isinstance(processed_data, np.ndarray)
    assert processed_data.shape[1] == sample_data.shape[1]

def test_model_training(sample_data):
    model = MarketPredictionModel()
    features = sample_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI']]
    target = sample_data['Close'].shift(-1)[:-1]
    
    metrics = model.train(features[:-1], target)
    assert 'mse' in metrics
    assert 'rmse' in metrics
    assert 'r2' in metrics
    assert 0 <= metrics['r2'] <= 1

def test_prediction(sample_data):
    model = MarketPredictionModel()
    features = sample_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI']]
    target = sample_data['Close'].shift(-1)[:-1]
    
    # Train model
    model.train(features[:-1], target)
    
    # Make prediction
    latest_features = features.iloc[-1:]
    prediction, confidence = model.predict(latest_features)
    
    assert isinstance(prediction, np.ndarray)
    assert isinstance(confidence, np.ndarray)
    assert 0 <= confidence[0] <= 1 