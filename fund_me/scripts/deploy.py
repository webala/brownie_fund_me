from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account
from web3 import Web3

def deploy_fund_me():
    account = get_account()

    if not network.show_active() == "development":
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]  # price feed address for persistent network(rinkeby)
    else:
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks ...")
        mock_aggregator = MockV3Aggregator.deploy(
            18, Web3.toWei(2000, 'ether'), {"from": account}
        )
        print("Mocks deployed")
        price_feed_address = mock_aggregator.address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},  # pass price feed to fund me constructor
        publish_source=config["networks"][network.show_active()].get("verify"), # source code will be published
    )  
    print(f"Fund me deployed at {fund_me.address}")


def main():
    deploy_fund_me()
