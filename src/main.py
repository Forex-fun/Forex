from models.prediction_model import MarketPredictionModel
from blockchain.smart_contract import PredictionContract
from data.market_data import MarketDataFetcher
import config
import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PredictionMarket:
    def __init__(self):
        self.market_data = MarketDataFetcher()
        self.prediction_model = MarketPredictionModel()
        self.blockchain_contract = PredictionContract(
            config.CONTRACT_ADDRESS,
            config.CONTRACT_ABI_PATH
        )
        
    def train_models(self, symbols=['BTC-USD', 'ETH-USD']):
        logger.info(f"Training models for symbols: {symbols}")
        results = {}
        
        data_dict = self.market_data.fetch_multiple_symbols(symbols)
        for symbol, data in data_dict.items():
            try:
                features = self._prepare_features(data)
                target = data['Close'].shift(-1)  # Next day's closing price
                
                # Remove last row since we don't have target for it
                features = features[:-1]
                target = target[:-1].values
                
                # Train model and get metrics
                metrics = self.prediction_model.train(features, target)
                logger.info(f"Training metrics for {symbol}: {metrics}")
                
                # Save trained model
                model_path = f"{config.MODEL_SAVE_PATH}/{symbol}_{datetime.now().strftime('%Y%m%d')}.joblib"
                self.prediction_model.save_model(model_path)
                
                results[symbol] = metrics
                
            except Exception as e:
                logger.error(f"Error training model for {symbol}: {str(e)}")
                results[symbol] = {'error': str(e)}
                
        return results
    
    def make_prediction(self, symbol):
        try:
            # Fetch latest data
            data = self.market_data.fetch_historical_data(symbol, period='60d')
            features = self._prepare_features(data)
            
            # Get prediction and confidence
            latest_features = features.iloc[-1:]
            prediction, confidence = self.prediction_model.predict(latest_features)
            
            current_price = data['Close'].iloc[-1]
            predicted_change = ((prediction[0] - current_price) / current_price) * 100
            
            result = {
                'symbol': symbol,
                'current_price': current_price,
                'predicted_price': prediction[0],
                'predicted_change_percent': predicted_change,
                'confidence_score': confidence[0],
                'timestamp': datetime.now().isoformat()
            }
            
            # If confidence is high enough, submit to blockchain
            if confidence[0] > config.PREDICTION_THRESHOLD:
                txn = self.blockchain_contract.place_prediction(
                    config.TRADING_ACCOUNT,
                    prediction[0],
                    config.DEFAULT_STAKE_AMOUNT
                )
                result['transaction_hash'] = txn['hash']
            
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction for {symbol}: {str(e)}")
            raise
    
    def _prepare_features(self, data):
        return data[[
            'Open', 'High', 'Low', 'Close', 'Volume',
            'SMA_20', 'SMA_50', 'RSI', 'MACD', 'Signal_Line',
            'BB_middle', 'BB_upper', 'BB_lower', 'Momentum',
            'Volatility', 'Volume_MA', 'Price_Momentum'
        ]]

def main():
    market = PredictionMarket()
    
    # Train models for multiple symbols
    training_results = market.train_models()
    logger.info("Training results:", training_results)
    
    # Make predictions
    symbols = ['BTC-USD', 'ETH-USD']
    for symbol in symbols:
        try:
            prediction = market.make_prediction(symbol)
            logger.info(f"Prediction for {symbol}:", prediction)
        except Exception as e:
            logger.error(f"Failed to make prediction for {symbol}: {str(e)}")

if __name__ == "__main__":
    main() 