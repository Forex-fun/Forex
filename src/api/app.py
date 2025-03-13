from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import PredictionMarket
import config
from auth.jwt_handler import JWTHandler
from auth.models import UserCreate, UserLogin, Token
from visualization.market_charts import MarketVisualizer
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI(
    title="Market Prediction API",
    description="AI-powered market prediction API with blockchain integration",
    version="1.0.0"
)

market = PredictionMarket()

class PredictionRequest(BaseModel):
    symbol: str
    stake_amount: Optional[float] = None

class PredictionResponse(BaseModel):
    symbol: str
    current_price: float
    predicted_price: float
    predicted_change_percent: float
    confidence_score: float
    timestamp: str
    transaction_hash: Optional[str] = None

@app.post("/predict", response_model=PredictionResponse)
async def make_prediction(request: PredictionRequest):
    try:
        result = market.make_prediction(request.symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/train/{symbol}")
async def train_model(symbol: str):
    try:
        results = market.train_models([symbol])
        return {
            "status": "success",
            "training_metrics": results[symbol]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=User.hash_password(user.password),
        wallet_address=user.wallet_address
    )
    db.add(db_user)
    db.commit()
    
    # Create access token
    access_token = JWTHandler.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token}

@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = JWTHandler.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token}

@app.get("/chart/{symbol}")
async def get_market_chart(
    symbol: str,
    chart_type: str = "price",
    current_user: dict = Depends(JWTHandler.get_current_user)
):
    try:
        market_data = market.market_data.fetch_historical_data(symbol)
        predictions = [market.make_prediction(symbol)]
        
        if chart_type == "price":
            fig = MarketVisualizer.create_price_prediction_chart(market_data, predictions)
        else:
            fig = MarketVisualizer.create_technical_indicators_chart(market_data)
            
        return fig.to_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 