// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PredictionMarket is Ownable, ReentrancyGuard {
    struct Prediction {
        address user;
        string symbol;
        uint256 predictedPrice;
        uint256 timestamp;
        uint256 stake;
        bool resolved;
        bool won;
    }
    
    struct Market {
        string symbol;
        uint256 minimumStake;
        uint256 rewardMultiplier;
        bool active;
    }
    
    mapping(bytes32 => Market) public markets;
    mapping(bytes32 => Prediction[]) public predictions;
    mapping(address => uint256) public userBalances;
    
    IERC20 public stakingToken;
    uint256 public platformFee = 100; // 1% = 100
    
    event MarketCreated(string symbol, uint256 minimumStake, uint256 rewardMultiplier);
    event PredictionPlaced(address user, string symbol, uint256 predictedPrice, uint256 stake);
    event PredictionResolved(address user, string symbol, uint256 predictedPrice, uint256 actualPrice, bool won);
    
    constructor(address _stakingToken) {
        stakingToken = IERC20(_stakingToken);
    }
    
    function createMarket(
        string memory symbol,
        uint256 minimumStake,
        uint256 rewardMultiplier
    ) external onlyOwner {
        bytes32 marketId = keccak256(abi.encodePacked(symbol));
        require(!markets[marketId].active, "Market already exists");
        
        markets[marketId] = Market({
            symbol: symbol,
            minimumStake: minimumStake,
            rewardMultiplier: rewardMultiplier,
            active: true
        });
        
        emit MarketCreated(symbol, minimumStake, rewardMultiplier);
    }
    
    function placePrediction(
        string memory symbol,
        uint256 predictedPrice,
        uint256 stake
    ) external nonReentrant {
        bytes32 marketId = keccak256(abi.encodePacked(symbol));
        Market storage market = markets[marketId];
        require(market.active, "Market not active");
        require(stake >= market.minimumStake, "Stake too low");
        
        // Transfer tokens from user
        require(stakingToken.transferFrom(msg.sender, address(this), stake), "Transfer failed");
        
        predictions[marketId].push(Prediction({
            user: msg.sender,
            symbol: symbol,
            predictedPrice: predictedPrice,
            timestamp: block.timestamp,
            stake: stake,
            resolved: false,
            won: false
        }));
        
        emit PredictionPlaced(msg.sender, symbol, predictedPrice, stake);
    }
    
    function resolvePrediction(
        string memory symbol,
        uint256 actualPrice,
        uint256 predictionIndex
    ) external onlyOwner {
        bytes32 marketId = keccak256(abi.encodePacked(symbol));
        Prediction storage prediction = predictions[marketId][predictionIndex];
        require(!prediction.resolved, "Already resolved");
        
        // Calculate if prediction was correct (within 1% margin)
        uint256 priceDiff = actualPrice > prediction.predictedPrice ? 
            actualPrice - prediction.predictedPrice : 
            prediction.predictedPrice - actualPrice;
        
        bool won = (priceDiff * 100) / prediction.predictedPrice <= 1;
        prediction.resolved = true;
        prediction.won = won;
        
        if (won) {
            uint256 reward = (prediction.stake * markets[marketId].rewardMultiplier) / 100;
            userBalances[prediction.user] += reward;
        }
        
        emit PredictionResolved(
            prediction.user,
            symbol,
            prediction.predictedPrice,
            actualPrice,
            won
        );
    }
    
    function withdraw() external nonReentrant {
        uint256 amount = userBalances[msg.sender];
        require(amount > 0, "No balance to withdraw");
        
        userBalances[msg.sender] = 0;
        require(stakingToken.transfer(msg.sender, amount), "Transfer failed");
    }
    
    function setPlatformFee(uint256 newFee) external onlyOwner {
        require(newFee <= 1000, "Fee too high"); // Max 10%
        platformFee = newFee;
    }
} 