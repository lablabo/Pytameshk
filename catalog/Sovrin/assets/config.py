import json


class config:

    pool_name = None
    genesis_file_path = None
    wallet_config = None
    wallet_credentials = None
    PROTOCOL_VERSION = None

    def __init__(self):

        self.pool_name = 'pool'
        self.genesis_file_path = '/home/mohammad/mohammad/indy-sdk/cli/docker_pool_transactions_genesis'
        self.wallet_config = json.dumps({"id": "wallet"})
        self.wallet_credentials = json.dumps({"key": "wallet_key"})
        # Set protocol version to 2 to work with the current version of Indy Node
        self.PROTOCOL_VERSION = 2

        pass


