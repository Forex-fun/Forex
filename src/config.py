import os

# Blockchain configuration
WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI", "http://localhost:8545")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")
CONTRACT_ABI_PATH = os.getenv("CONTRACT_ABI_PATH", "contracts/abi/PredictionMarket.json")
OWNER_PRIVATE_KEY = os.getenv("OWNER_PRIVATE_KEY", "your-private-key")
GAS_LIMIT = int(os.getenv("GAS_LIMIT", "2000000"))
TRADING_ACCOUNT = os.getenv("TRADING_ACCOUNT", "0x0000000000000000000000000000000000000000")
DEFAULT_STAKE_AMOUNT = float(os.getenv("DEFAULT_STAKE_AMOUNT", "0.1"))

# Model configuration
MODEL_SAVE_PATH = os.getenv("MODEL_SAVE_PATH", "models/saved_models/")
PREDICTION_THRESHOLD = float(os.getenv("PREDICTION_THRESHOLD", "0.7"))

# API configuration
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/prediction_market.log")

# Data configuration
CACHE_DURATION = int(os.getenv("CACHE_DURATION", "3600"))  # 1 hour in seconds
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "5"))

# Authentication configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prediction_market.db") 