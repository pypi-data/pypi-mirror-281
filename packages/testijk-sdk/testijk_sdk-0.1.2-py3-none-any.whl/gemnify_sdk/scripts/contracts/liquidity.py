from gemnify_sdk.scripts.instance import ContractInstance

class Liquidity:
    def __init__(self, config) -> None:
        self.instance = ContractInstance(config, 'RewardRouter')

    def add_liquidity(self, *args):
        return self.instance.create_transaction("mintAndStakeUlp", args)

    def remove_liquidity(self, *args):
        return self.instance.create_transaction("unstakeAndRedeemUlp", args)
