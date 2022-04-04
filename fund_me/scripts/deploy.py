from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_DEVELOPMENT_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    if not network.show_active() in LOCAL_DEVELOPMENT_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]  # price feed address for persistent network(rinkeby)
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address  # Use latest MockV3Aggregator

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},  # pass price feed to fund me constructor
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # source code will be published
    )
    print(f"Fund me deployed at {fund_me.address}")


def main():
    deploy_fund_me()
