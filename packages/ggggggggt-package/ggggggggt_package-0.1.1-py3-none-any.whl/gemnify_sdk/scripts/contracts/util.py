from gemnify_sdk.scripts.instance import ContractInstance, get_contract_address
from gemnify_sdk.scripts.utils import get_token_address
import time
from web3 import Web3
from gemnify_sdk.scripts.logging import getLogger

class Util:
    def __init__(self, config) -> None:
        self.web3 = Web3(Web3.HTTPProvider(config.rpc))
        self.config = config
        self.logger = getLogger(config)

    def mint_token(self, token_name, to_address, amount):
        token_address = get_token_address(token_name)
        instance = ContractInstance(self.config, 'Token', token_address)
        return instance.create_transaction("mint", [to_address, amount])

    # add liquidity
    def approve_token_to_ulp_manager(self, token_name, amount):
        token_address = get_token_address(token_name)
        instance = ContractInstance(self.config, 'Token', token_address)
        ulp_manger_address = get_contract_address("UlpManager")
        return instance.create_transaction("approve", [ulp_manger_address, amount])

    # swap
    def approve_token_to_router(self, token_name, amount):
        token_address = get_token_address(token_name)
        instance = ContractInstance(self.config, 'Token', token_address)
        ulp_manger_address = get_contract_address("Router")
        return instance.create_transaction("approve", [ulp_manger_address, amount])

    # position
    def approve_plugin_position_router(self):
        instance = ContractInstance(self.config, 'Router')
        position_router_address = get_contract_address("PositionRouter")
        return instance.create_transaction("approvePlugin", [position_router_address])

    # order
    def approve_plugin_order_book(self):
        instance = ContractInstance(self.config, 'Router')
        order_book_address = get_contract_address("OrderBook")
        return instance.create_transaction("approvePlugin", [order_book_address])

    def wait_for_confirmation(self, tx_hash, timeout=120, poll_interval=2):
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                if receipt is not None:
                    if receipt.status == 1:
                        self.logger.info(f"transaction {tx_hash} confirmed and successful")
                        return True
                    else:
                        self.logger.error(f"transaction {tx_hash} failed")
                        return False
            except Exception as e:
                self.logger.info(f"checking... {e}")

            time.sleep(poll_interval)

        self.logger.error(f"transaction {tx_hash} not confirmed within timeout period")
        return False
