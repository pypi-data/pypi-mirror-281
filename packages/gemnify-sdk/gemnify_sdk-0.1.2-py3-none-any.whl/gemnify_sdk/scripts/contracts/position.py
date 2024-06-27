from gemnify_sdk.scripts.instance import ContractInstance

class Position:
    def __init__(self, config) -> None:
        self.instance = ContractInstance(config, 'PositionRouter')

    def create_increase_position(self, *args, value):
        return self.instance.create_transaction("createIncreasePosition", args, value)

    def cancel_increase_position(self, *args):
        return self.instance.create_transaction("cancelIncreasePosition", args)

    def create_decrease_position(self, *args):
        return self.instance.create_transaction("createDecreasePosition", args)

    def cancel_decrease_position(self, *args):
        return self.instance.create_transaction("cancelDecreasePosition", args)
