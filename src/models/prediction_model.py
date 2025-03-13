from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import joblib

class MarketPredictionModel:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def preprocess_data(self, data):
        if isinstance(data, pd.DataFrame):
            # Add more technical indicators
            data = self._add_technical_indicators(data)
            data = data.values
        return self.scaler.fit_transform(data)
    
    def _add_technical_indicators(self, df):
        # Add MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # Add Bollinger Bands
        df['BB_middle'] = df['Close'].rolling(window=20).mean()
        df['BB_upper'] = df['BB_middle'] + 2 * df['Close'].rolling(window=20).std()
        df['BB_lower'] = df['BB_middle'] - 2 * df['Close'].rolling(window=20).std()
        
        # Add momentum
        df['Momentum'] = df['Close'] - df['Close'].shift(4)
        
        return df.fillna(0)
    
    def train(self, X, y):
        X_scaled = self.preprocess_data(X)
        self.model.fit(X_scaled, y)
        
        # Calculate training metrics
        y_pred = self.model.predict(X_scaled)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        
        return {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'r2': r2
        }
    
    def predict(self, X):
        X_scaled = self.preprocess_data(X)
        predictions = self.model.predict(X_scaled)
        
        # Add confidence scores based on feature importance
        confidence_scores = self._calculate_confidence(X_scaled)
        
        return predictions, confidence_scores
    
    def _calculate_confidence(self, X):
        feature_importance = self.model.feature_importances_
        # Weight predictions by feature importance
        confidence = np.mean(X * feature_importance, axis=1)
        return np.clip(confidence, 0, 1)
    
    def save_model(self, path):
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, path)
    
    def load_model(self, path):
        saved_data = joblib.load(path)
        self.model = saved_data['model']
        self.scaler = saved_data['scaler'] 