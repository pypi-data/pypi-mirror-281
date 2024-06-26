from gemnify_sdk.scripts.instance import ContractInstance

class Swap:
    def __init__(self, config) -> None:
        self.instance = ContractInstance('orderbook', config)
