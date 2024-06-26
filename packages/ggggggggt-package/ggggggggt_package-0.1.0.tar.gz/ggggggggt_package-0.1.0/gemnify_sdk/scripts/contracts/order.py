from gemnify_sdk.scripts.instance import ContractInstance

class Order:
    def __init__(self, config) -> None:
        self.instance = ContractInstance('OrderBook', config)

    def create_increase_order(self, *args, value):
        self.instance.create_transaction("createIncreaseOrder", args, value)

    def update_increase_order(self):
        pass

    def cancel_increase_order(self):
        pass

    def create_decrease_order(self):
        pass

    def update_decrease_order(self):
        pass

    def cancel_decrease_order(self):
        pass

    def cancel_multiple(self):
        pass

    def create_swap_order(self):
        pass

    def update_swap_order(self):
        pass

    def cancel_swap_order(self):
        pass

    def get_increase_order(self, *args):
        return self.instance.call_function("getIncreaseOrder", args)

    def get_decrease_order(self):
        pass

    def get_swap_order(self):
        pass

    def min_execution_fee(self):
        pass

    def validate_position_order_price(self):
        pass

    def decrease_orders(self):
        pass

    def increase_orders(self):
        pass

    def swap_orders(self):
        pass