from gemnify_sdk.scripts.contracts import order, position, liquidity, swap, util

class Gemnify:
    def __init__(self, config):
        self.config = config

    def order(self):
        return order.Order(self.config)

    def position(self):
        return position.Position(self.config)

    def liquidity(self):
        return liquidity.Liquidity(self.config)

    def swap(self):
        return swap.Swap(self.config)

    def util(self):
        return util.Util(self.config)