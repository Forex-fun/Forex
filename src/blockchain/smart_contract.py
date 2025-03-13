from web3 import Web3
import json

class PredictionContract:
    def __init__(self, contract_address, abi_path):
        self.w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
        self.contract_address = contract_address
        
        with open(abi_path) as f:
            contract_abi = json.load(f)
        
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=contract_abi
        )
    
    def place_prediction(self, user_address, prediction_value, stake_amount):
        nonce = self.w3.eth.get_transaction_count(user_address)
        
        txn = self.contract.functions.placePrediction(
            prediction_value
        ).build_transaction({
            'from': user_address,
            'value': stake_amount,
            'gas': 2000000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': nonce,
        })
        
        return txn
    
    def get_prediction_result(self, prediction_id):
        return self.contract.functions.getPredictionResult(prediction_id).call() 