from gemnify_sdk.scripts.instance import ContractInstance

class Order:
    def __init__(self, config) -> None:
        self.instance = ContractInstance(config, 'OrderBook')

    def create_increase_order(self, *args, value):
        return self.instance.create_transaction("createIncreaseOrder", args, value)

    def update_increase_order(self, *args):
        return self.instance.create_transaction("updateIncreaseOrder", args)

    def cancel_increase_order(self, *args):
        return self.instance.create_transaction("cancelIncreaseOrder", args)

    def create_decrease_order(self, *args, value):
        return self.instance.create_transaction("createDecreaseOrder", args, value)

    def update_decrease_order(self, *args):
        return self.instance.create_transaction("updateDecreaseOrder", args)

    def cancel_decrease_order(self, *args):
        return self.instance.create_transaction("cancelDecreaseOrder", args)

    def cancel_multiple(self, *args):
        pass

    def create_swap_order(self, *args):
        pass

    def update_swap_order(self, *args):
        pass

    def cancel_swap_order(self, *args):
        pass

    def get_increase_order(self, *args):
        return self.instance.call_function("getIncreaseOrder", args)

    def get_decrease_order(self, *args):
        pass

    def get_swap_order(self, *args):
        pass

    def min_execution_fee(self, *args):
        pass

    def validate_position_order_price(self, *args):
        pass

    def decrease_orders(self, *args):
        pass

    def increase_orders(self, *args):
        pass

    def swap_orders(self, *args):
        pass