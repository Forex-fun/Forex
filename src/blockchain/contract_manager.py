from web3 import Web3
from eth_account import Account
import json
import logging
from typing import Dict, Optional
import config

logger = logging.getLogger(__name__)

class ContractManager:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(config.WEB3_PROVIDER_URI))
        
        with open(config.CONTRACT_ABI_PATH) as f:
            self.contract_abi = json.load(f)
            
        self.contract = self.w3.eth.contract(
            address=config.CONTRACT_ADDRESS,
            abi=self.contract_abi
        )
        
    def create_market(
        self,
        symbol: str,
        minimum_stake: int,
        reward_multiplier: int,
        private_key: str
    ) -> Dict:
        try:
            account = Account.from_key(private_key)
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            txn = self.contract.functions.createMarket(
                symbol,
                minimum_stake,
                reward_multiplier
            ).build_transaction({
                'from': account.address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(txn, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return {
                'status': 'success',
                'transaction_hash': receipt['transactionHash'].hex(),
                'block_number': receipt['blockNumber']
            }
            
        except Exception as e:
            logger.error(f"Error creating market: {str(e)}")
            raise
            
    def place_prediction(
        self,
        symbol: str,
        predicted_price: int,
        stake_amount: int,
        private_key: str
    ) -> Dict:
        try:
            account = Account.from_key(private_key)
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            txn = self.contract.functions.placePrediction(
                symbol,
                predicted_price,
                stake_amount
            ).build_transaction({
                'from': account.address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(txn, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return {
                'status': 'success',
                'transaction_hash': receipt['transactionHash'].hex(),
                'block_number': receipt['blockNumber']
            }
            
        except Exception as e:
            logger.error(f"Error placing prediction: {str(e)}")
            raise
            
    def get_market_info(self, symbol: str) -> Dict:
        try:
            market_id = Web3.solidity_keccak(['string'], [symbol])
            market = self.contract.functions.markets(market_id).call()
            
            return {
                'symbol': market[0],
                'minimum_stake': market[1],
                'reward_multiplier': market[2],
                'active': market[3]
            }
        except Exception as e:
            logger.error(f"Error getting market info: {str(e)}")
            raise 