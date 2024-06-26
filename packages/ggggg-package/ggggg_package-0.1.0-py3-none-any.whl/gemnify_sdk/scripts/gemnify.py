from gemnify_sdk.scripts.contracts import order, position, liquidity

class Gemnify:
    def __init__(self, config):
        self.config = config

    def order(self):
        return order.Order(self.config)

    def position(self):
        return position.Position(self.config)

    def liquidity(self):
        return liquidity.Liquidity(self.config)