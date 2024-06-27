from gemnify_sdk.scripts.utils import create_connection, get_contract_object

class GetAddress:
    def __init__(self, *args: list, **kwargs: dict) -> None:
        self.AddressDict = {
            "usdc": "",
            "OrderBook": "0x1718C9E2EE4Ac042e03A92783B3cAA7B0D927464",
            "PositionRouter": "0x1a5988A9d7aD5262c9f60DdE4866896cb38fe70a"
        }