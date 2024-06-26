class Config:
    def __init__(self, chain: str):
        self.chain = chain
        self.rpc = None
        self.chain_id = None
        self.user_wallet_address = None
        self.private_key = None
        self.tg_bot_token = None

    def set_rpc(self, value):
        self.rpc = value

    def set_chain_id(self, value):
        self.chain_id = value

    def set_wallet_address(self, value):
        self.user_wallet_address = value

    def set_private_key(self, value):
        self.private_key = value