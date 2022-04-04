from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3


DECIMALS = 18
STARTING_PRICE = 2000
LOCAL_DEVELOPMENT_ENVIRONMENTS =['development', 'ganache-local']


def get_account():
    if network.show_active() in LOCAL_DEVELOPMENT_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks ...")
    if len(MockV3Aggregator) <= 0:
        # check if there is a MockV3Aggregator deployed in the same network
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
        )
        print("Mocks deployed")
