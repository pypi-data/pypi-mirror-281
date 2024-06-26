from web3 import Web3
from gemnify_sdk.scripts.utils import get_contract_address, get_contract_abi
from gemnify_sdk.scripts.utils import get_address_from_private_key

class ContractInstance:
    def __init__(self, contract_name, config) -> None:
        web3_obj = Web3(Web3.HTTPProvider(config.rpc))

        self.contract = get_contract_object(
            web3_obj,
            contract_name,
            config.chain
        )
        self.web3 = web3_obj
        self.config = config

    def create_transaction(self, fn_name, args, value = 0):
        tx_data = self.generate_transaction_data(
            fn_name = fn_name,
            args = args  # array
        )
        return self.submit_transaction(tx_data, value)

    def generate_transaction_data(self, fn_name, args):
        return self.contract.encodeABI(
            fn_name = fn_name,
            args = args
        )

    def submit_transaction(self, tx_data, value):
        sender_address = get_address_from_private_key(self.config.private_key)
        nonce = self.web3.eth.get_transaction_count(sender_address)
        gas_price = self.web3.eth.gas_price
        gas_estimate = self.web3.eth.estimate_gas({
            'from': sender_address,
            'to': self.contract.address,
            'value': value,  # wei
            'data': tx_data
        })

        transaction = {
            'to': self.contract.address,
            'value': self.web3.to_wei(value, 'wei'),
            'gas': gas_estimate,  # gas limit
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data,
            'chainId': self.web3.eth.chain_id
        }

        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=self.config.private_key)

        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"Transaction hash: {tx_hash.hex()}")
        return tx_hash.hex()

    def call_function(self, fn_name, args):
        try:
            result = self.contract.functions[fn_name](*args).call()
            return result
        except Exception as e:
            print(f"Error calling function {fn_name}: {e}")
            return None

def get_contract_object(web3_obj, contract_name: str, chain: str):
    """
    Using a contract name, retrieve the address and api and create a web3 contract object

    Parameters
    ----------
    web3_obj : web3_obj
        web3 connection.
    contract_name : str
        name of contract to use to map.
    chain : str
        chain name.

    Returns
    -------
    contract_obj
        an instantied web3 contract object.

    """

    contract_address = get_contract_address(contract_name, chain)
    contract_abi = get_contract_abi(contract_name)

    return web3_obj.eth.contract(
        address=contract_address,
        abi=contract_abi
    )
