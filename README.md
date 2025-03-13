# Forex - AI-Powered Market Prediction Platform

Forex is an intelligent market prediction platform that combines AI and blockchain technology to provide users with smart market trend analysis and prediction services.

## Features

### AI Prediction Engine
- Market prediction using Random Forest algorithm
- Multi-dimensional technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Prediction confidence scoring system
- Automated model training and updates

### Blockchain Integration
- Smart contracts for transaction transparency
- Decentralized prediction markets
- ERC20 token-based reward system
- Automated settlement system

### User Features
- Real-time market data visualization
- Personalized prediction dashboard
- Historical prediction tracking
- Multi-currency support (BTC, ETH, etc.)

## Tech Stack

### Backend
- Python 3.9
- FastAPI
- SQLAlchemy
- scikit-learn
- Web3.py

### Frontend
- React
- TypeScript
- Plotly.js
- React Query

### Blockchain
- Solidity
- OpenZeppelin
- Ganache
- Web3.js

### Deployment
- Docker
- PostgreSQL
- Nginx
- GitHub Actions

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker & Docker Compose
- PostgreSQL 13+

### Installation

1. Clone the repository
```bash
git clone https://github.com/Forex-me/Forex.git
cd forex
```

2. Install dependencies
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
```

3. Configure environment
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

4. Start services
```bash
# Start all services using Docker Compose
docker-compose up -d
```

5. Access the application
- API Documentation: http://localhost:8000/docs
- Frontend Interface: http://localhost:3000

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d
```

## Development Guide

### Project Structure
```
forex/
├── src/
│   ├── api/          # FastAPI application
│   ├── models/       # AI models
│   ├── blockchain/   # Blockchain interaction
│   └── data/         # Data processing
├── contracts/        # Smart contracts
├── frontend/         # React frontend
├── tests/           # Test cases
└── docker/          # Docker configuration
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_prediction_model.py
```

### Code Standards
- Code formatting with black
- Code linting with flake8
- Type checking with mypy

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

 [Twitter](https://x.com/Forex_Credible)

